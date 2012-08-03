![](https://raw.github.com/mkwiatkowski/mandelbrot/master/mandelbrot.png)

This script was an experiment in using C extensions with Python. Generating [Mandelbrot set](http://en.wikipedia.org/wiki/Mandelbrot_set) visualization is expensive, so coding a C extension for that was a perfect fit. Another neat thing about this program is that it will run fine without a compiled extension, although much slower.

For good performance, first compile the C extension with:

    make

Now, wasn't that easy. ;-) To run the program do:

    python mandelbrot.py

If you feel you can improve its performance even more, use the profiler first:

    python mandelbrot.py prof

Written in November 2007.

Copyleft: Michał Kwiatkowski
License: MIT
