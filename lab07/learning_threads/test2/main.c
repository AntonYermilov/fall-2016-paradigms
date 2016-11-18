#include <pthread.h>
#include <stdlib.h>
#include <stdio.h>

void* process(void* param) {
	for (int i = 0; i < 100; i++)
		printf("%d\n", *(int*)(param));
	return NULL;
}

int main(int argc, char** argv) {
	int x = atoi(argv[1]);
	int y = atoi(argv[2]);

	pthread_t my_thread1, my_thread2;
	if (pthread_create(&my_thread1, NULL, process, &x)) {
		fprintf(stderr, "Error creating thread #1\n");
		return 1;
	}
	if (pthread_create(&my_thread2, NULL, process, &y)) {
		fprintf(stderr, "Error creating thread #2\n");
		return 1;
	}

	printf("How it works?!\n");

	if (pthread_join(my_thread1, NULL)) {
		fprintf(stderr, "Error joining thread #1\n");
		return 2;
	}
	if (pthread_join(my_thread2, NULL)) {
		fprintf(stderr, "Error joining thread #2\n");
		return 2;
	}

	return 0;
}
