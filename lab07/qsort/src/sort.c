#include "sort.h"
#include "thread_pool.h"

sort_task_t* sort_task_create(int* array, int len, int depth) {
	sort_task_t* task = malloc(sizeof(sort_task_t));
	task->array = array;
	task->len = len;
	task->depth = depth;
	return task;
}

static int compare(const void* a, const void* b) {
	int* pta = (int*)(a);
	int* ptb = (int*)(b);
	return *pta - *ptb;
}

void sort(void* data) {
	task_t* task = (task_t*)(data);
	sort_task_t* sort_task = (sort_task_t*)(task->args);

	if (sort_task->len <= 1)
		return;
	if (sort_task->depth == 0) {
		qsort(sort_task->array, sort_task->len, sizeof(int), compare);
		return;
	}

	int partition = sort_task->array[rand() % sort_task->len];
	int* copy = malloc(sort_task->len * sizeof(int));

	int l = 0, r = sort_task->len;
	for (int i = 0; i < sort_task->len; i++) {
		if (sort_task->array[i] <= partition) {
			copy[l++] = sort_task->array[i];
		} else {
			copy[--r] = sort_task->array[i];
		}
	}

	//while (l > 1 && copy[l - 1] == copy[l - 2])
	//	l--;
	//l--;

	memcpy(sort_task->array, copy, sizeof(int) * sort_task->len);
	free(copy);

	sort_task_t* sort_task_l = sort_task_create(sort_task->array, l, sort_task->depth - 1);
	sort_task_t* sort_task_r = sort_task_create(sort_task->array + l, sort_task->len - l, sort_task->depth - 1);

	task_t* task_l = task_create(task->pool, sort, (void*)(sort_task_l));
	task_t* task_r = task_create(task->pool, sort, (void*)(sort_task_r));
	task->left = task_l;
	task->right = task_r;

	thpool_submit(task->pool, task_l);
	thpool_submit(task->pool, task_r);
}
