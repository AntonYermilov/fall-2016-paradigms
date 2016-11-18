#ifndef __SORT_H__
#define __SORT_H__

#include <stdlib.h>
#include <string.h>

typedef struct sort_task {
	int* array;
	int len;
	int depth;
} sort_task_t;

sort_task_t* sort_task_create(int* array, int len, int depth);
void sort(void* data);

#endif
