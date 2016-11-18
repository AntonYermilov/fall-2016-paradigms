main: src/main.c src/thread_pool.c src/sort.c src/queue.c src/squeue.c
	gcc src/main.c src/thread_pool.c src/sort.c src/queue.c src/squeue.c -I include/ -o main -lpthread

clean:
	rm -f main
	rm -f src/*~
	rm -f src/*.swp
	rm -f include/*~
	rm -f include/*.swp
