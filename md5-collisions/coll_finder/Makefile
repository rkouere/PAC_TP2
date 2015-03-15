.PHONY: clean

coll_finder: lib/libcoll.a md5.o main.o
	g++ lib/*.o *.o -o coll_finder

lib/libcoll.a:
	cd lib && $(MAKE)

clean:
	rm -f coll_finder
	rm -f *.o
	cd lib && $(MAKE) clean
