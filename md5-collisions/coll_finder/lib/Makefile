OBJ=block0.o block1stevens00.o block1stevens10.o block1wang.o md5.o block1.o block1stevens01.o block1stevens11.o main.o

.PHONY: clean

CXX=g++
CPPFLAGS=-O3

libcoll.a: $(OBJ)
	ar rcs libcoll.a $(OBJ)

clean:
	rm -f *.a
	rm -f *.o
