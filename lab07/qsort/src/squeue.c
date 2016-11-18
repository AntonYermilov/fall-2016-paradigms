/*SAFE QUEUE FOR THREADS*/

#include "squeue.h"

void squeue_init(squeue_t* queue) {
	queue_init(&queue->queue);
	pthread_mutex_init(&queue->mutex, NULL);
	pthread_cond_init(&queue->cond, NULL);
}

void squeue_push(squeue_t* queue, node_t* node) {
	pthread_mutex_lock(&queue->mutex);
	queue_push(&queue->queue, node);
	pthread_cond_signal(&queue->cond);
	pthread_mutex_unlock(&queue->mutex);
}

node_t* squeue_pop(squeue_t* queue) {
	pthread_mutex_lock(&queue->mutex);
	node_t* node = queue_pop(&queue->queue);
	pthread_mutex_unlock(&queue->mutex);
	return node;
}

int squeue_size(squeue_t* queue) {
	return queue_size(&queue->queue);
}

void squeue_finit(squeue_t* queue) {
	pthread_mutex_destroy(&queue->mutex);
	pthread_cond_destroy(&queue->cond);
}

void squeue_notify(squeue_t* queue) {
	pthread_mutex_lock(&queue->mutex);
	pthread_cond_signal(&queue->cond);
	pthread_mutex_unlock(&queue->mutex);
}

void squeue_notify_all(squeue_t* queue) {
	pthread_mutex_lock(&queue->mutex);
	pthread_cond_broadcast(&queue->cond);
	pthread_mutex_unlock(&queue->mutex);
}
