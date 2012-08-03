all: _mandelbrot.c
	gcc _mandelbrot.c -I/usr/include/python2.7/ -fPIC -Wall -O3 -c -o _mandelbrot.o
	gcc -shared _mandelbrot.o -o _mandelbrot.so

clean:
	rm -f _mandelbrot.o _mandelbrot.so hotshot_mandel_stats mandelbrot.pyc
