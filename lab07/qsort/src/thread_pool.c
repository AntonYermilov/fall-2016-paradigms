#include "thread_pool.h"

static volatile int cont = 1;

static void* process(void* data) {
	squeue_t* queue = (squeue_t*)(data);

	while (cont || squeue_size(queue)) {
		pthread_mutex_lock(&queue->mutex);
		while (cont && !squeue_size(queue))
			pthread_cond_wait(&queue->cond, &queue->mutex);
		node_t* node = queue_pop(&queue->queue);
		pthread_mutex_unlock(&queue->mutex);

		if (node) {
			task_t* task = (task_t*)(node);

			pthread_mutex_lock(&task->mutex);
				task->func((void*)(task));
				task->finished = true;
				pthread_cond_signal(&task->cond);
				pthread_mutex_unlock(&task->mutex);
			}
		}

		return NULL;
	}

	task_t* task_create(thread_pool_t* pool, void (*func)(void*), void* args) {
		task_t* task = malloc(sizeof(task_t));
		task->pool = pool;
		task->func = func;
		task->args = args;
		task->finished = false;
		task->left = task->right = NULL;
		pthread_mutex_init(&task->mutex, NULL);
		pthread_cond_init(&task->cond, NULL);
		return task;
	}

	void thpool_init(thread_pool_t* pool, uint16_t threads_nm) {
	squeue_init(&pool->queue);

	pool->threads = malloc(threads_nm * sizeof(pthread_t));
	pool->threads_nm = threads_nm;
	for (int i = 0; i < threads_nm; i++)
		pthread_create(&pool->threads[i], NULL, process, &pool->queue);
}

void thpool_submit(thread_pool_t* pool, task_t* task) {
	squeue_push(&pool->queue, (node_t*)(task));
}

void thpool_wait(task_t* task) {
	if (!task)
		return;
	pthread_mutex_lock(&task->mutex);
	while (!task->finished)
		pthread_cond_wait(&task->cond, &task->mutex);
	pthread_mutex_unlock(&task->mutex);
}

void thpool_finit(thread_pool_t* pool) {
	pthread_mutex_lock(&pool->queue.mutex);
	cont = 0;
	pthread_mutex_unlock(&pool->queue.mutex);
	
	squeue_notify_all(&pool->queue);
	for (int i = 0; i < pool->threads_nm; i++)
		pthread_join(pool->threads[i], NULL);
	free(pool->threads);
	squeue_finit(&pool->queue);
}
