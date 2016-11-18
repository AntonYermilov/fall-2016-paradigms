#include <pthread.h>
#include <stdlib.h>
#include <stdio.h>

void* process(void* param) {
	printf("Hello World %d!\n", *(int*)(param));
	return NULL;
}

int main(int argc, char** argv) {
	int value = atoi(argv[1]);

	pthread_t my_thread;
	if (pthread_create(&my_thread, NULL, process, &value)) {
		fprintf(stderr, "Error creating thread\n");
		return 1;
	}

	printf("How it works?!\n");

	if (pthread_join(my_thread, NULL)) {
		fprintf(stderr, "Error joining thread\n");
		return 2;
	}

	return 0;
}
