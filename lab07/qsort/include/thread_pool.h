#ifndef __THREAD_POOL__
#define __THREAD_POOL__

#include <pthread.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include "squeue.h"

typedef struct thread_pool {
	pthread_t* threads;
	uint16_t threads_nm;
	squeue_t queue;
} thread_pool_t;

typedef struct task {
	node_t node;
	void (*func)(void*);
	void* args;
	bool finished;

	struct task* left;
	struct task* right;

	thread_pool_t* pool;
	pthread_mutex_t mutex;
	pthread_cond_t cond;
} task_t;

task_t* task_create(thread_pool_t* pool, void (*func)(void*), void* args);

void thpool_init(thread_pool_t* pool, uint16_t threads_nm);
void thpool_submit(thread_pool_t* pool, task_t* task);
void thpool_wait(task_t* task);
void thpool_finit(thread_pool_t* pool);

#endif
