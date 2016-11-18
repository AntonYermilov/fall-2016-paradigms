#ifndef __SQUEUE_H__
#define __SQUEUE_H__

#include <pthread.h>
#include "queue.h"

typedef struct squeue {
	queue_t queue;
	pthread_mutex_t mutex;
	pthread_cond_t cond;
} squeue_t;

void squeue_init(squeue_t* queue);
void squeue_push(squeue_t* queue, node_t* node);
node_t* squeue_pop(squeue_t* queue);
int squeue_size(squeue_t* queue);
void squeue_finit(squeue_t* queue);

void squeue_notify(squeue_t* queue);
void squeue_notify_all(squeue_t* queue);

#endif
