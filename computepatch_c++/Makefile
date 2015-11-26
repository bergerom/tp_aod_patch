CC = g++
CFLAGS = -Wall -std=c++11

patchAtom.o: patchAtom.cpp patchAtom.hpp
	$(CC) -c $< $(CFLAGS)

patch.o: patch.cpp patch.hpp patchAtom.hpp
	$(CC) -c $< $(CFLAGS)

computePatch.o: computePatch.cpp computePatch.hpp patch.hpp patchAtom.hpp
	$(CC) -c $< $(CFLAGS)

clean:
	rm -rf *.o
