#ifndef __QUEUE_H__
#define __QUEUE_H__

#include <stddef.h>

typedef struct node {
	struct node* next;
	struct node* prev;
} node_t;

typedef struct queue {
	node_t head;
	int size;
} queue_t;

void queue_init(queue_t* queue);
void queue_push(queue_t* queue, node_t* node);
node_t* queue_pop(queue_t* queue);
int queue_size(queue_t* queue);

#endif
