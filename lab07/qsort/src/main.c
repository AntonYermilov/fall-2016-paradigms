#include <stdlib.h>
#include <stdio.h>
#include <assert.h>

#include "thread_pool.h"
#include "sort.h"

void dfs(task_t* task) {
	if (task == NULL)
		return;
	thpool_wait(task);
	dfs(task->left);
	dfs(task->right);
	free(task->args);
	free(task);
}

int check(int* array, int size) {
	for (int i = 0; i < size - 1; i++)
		if (array[i] > array[i + 1])
			return 0;
	return 1;
}

void print_data(int* array, int size) {
	for (int i = 0; i < size; i++)
		printf("%d ", array[i]);
	printf("\n");
}

int main(int argc, char** argv) {
	uint16_t threads_nm = atoi(argv[1]);
	int n = atoi(argv[2]);
	int maxdep = atoi(argv[3]);
	
	srand(566);
	int* array = malloc(n * sizeof(int));
	for (int i = 0; i < n; i++)
		array[i] = rand();

	thread_pool_t pool;
	thpool_init(&pool, threads_nm);

	task_t* task = task_create(&pool, sort, (void*)(sort_task_create(array, n, maxdep)));
	thpool_submit(&pool, task);
	
	dfs(task);
	
	int correct = check(array, n);
	assert(correct);
	
	thpool_finit(&pool);

	free(array);
	pthread_exit(NULL);

	return 0;
}
