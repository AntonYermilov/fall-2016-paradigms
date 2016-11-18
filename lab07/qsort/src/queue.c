#include "queue.h"
#include "assert.h"

void queue_init(queue_t* queue) {
	queue->head.next = &queue->head;
	queue->head.prev = &queue->head;
	queue->size = 0;
}

void queue_push(queue_t* queue, node_t* node) {
	node->prev = &queue->head;
	node->next = queue->head.next;
	node->prev->next = node;
	node->next->prev = node;
	queue->size++;
}

node_t* queue_pop(queue_t* queue) {
	if (!queue_size(queue))
		return NULL;
	node_t* front = queue->head.prev;
	front->prev->next = front->next;
	front->next->prev = front->prev;
	queue->size--;
	return front;
}

int queue_size(queue_t* queue) {
	return queue->size;
}
