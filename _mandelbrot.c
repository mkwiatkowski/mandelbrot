#include <Python.h>

inline double in_mandelbrot_set(double cx, double cy, int max_iterations) {
  double x, y, tmp;
  int i;

  x = cx;
  y = cy;

  for (i=0; i < max_iterations; i++) {
    tmp = x*x - y*y + cx;
    y   = 2*x*y + cy;
    x   = tmp;
    if (x*x + y*y > 4) {
      break;
    }
  }

  return i / (double)max_iterations;
}

inline long get_screen_width(PyObject *screen) {
  PyObject *screen_width_object = PyObject_GetAttrString(screen, "width");
  long screen_width = PyInt_AsLong(screen_width_object);
  Py_DECREF(screen_width_object);
  return screen_width;
}

inline long get_screen_height(PyObject *screen) {
  PyObject *screen_height_object = PyObject_GetAttrString(screen, "height");
  long screen_height = PyInt_AsLong(screen_height_object);
  Py_DECREF(screen_height_object);
  return screen_height;
}

inline double get_screen_scale(PyObject *screen) {
  PyObject *screen_scale_object = PyObject_GetAttrString(screen, "scale");
  double screen_scale = PyFloat_AsDouble(screen_scale_object);
  Py_DECREF(screen_scale_object);
  return screen_scale;
}

inline double get_screen_left_cord(PyObject *screen) {
  PyObject *screen_left_cord_object = PyObject_GetAttrString(screen, "left_cord");
  double screen_left_cord = PyFloat_AsDouble(screen_left_cord_object);
  Py_DECREF(screen_left_cord_object);
  return screen_left_cord;
}

inline double get_screen_top_cord(PyObject *screen) {
  PyObject *screen_top_cord_object = PyObject_GetAttrString(screen, "top_cord");
  double screen_top_cord = PyFloat_AsDouble(screen_top_cord_object);
  Py_DECREF(screen_top_cord_object);
  return screen_top_cord;
}

static PyObject *color_for_pixel(PyObject *self, PyObject *args) {
  int pixel_x, pixel_y, max_iterations;
  PyObject *screen;

  if (!PyArg_ParseTuple(args, "(ii)iO", &pixel_x, &pixel_y, &max_iterations, &screen))
    return NULL;

  int screen_width  = get_screen_width(screen);
  int screen_height = get_screen_height(screen);
  double scale       = get_screen_scale(screen);
  double left_cord   = get_screen_left_cord(screen);
  double top_cord    = get_screen_top_cord(screen);

  /* pixel_to_point */
  double point_x = 1.25/scale*pixel_x/(screen_width-1) + left_cord;
  double point_y = 1.0/scale*pixel_y/(screen_height-1) - top_cord;
  /* in_mandelbrot_set */
  double certainty = in_mandelbrot_set(point_x, point_y, max_iterations);
  /* make_color */
  int shade = 255 * certainty;

  return Py_BuildValue("(iii)", shade, shade, shade);
}

static PyMethodDef mandelbrot_methods[] = {
  {"color_for_pixel", color_for_pixel, METH_VARARGS, ""},
  {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC init_mandelbrot(void)
{
  (void) Py_InitModule("_mandelbrot", mandelbrot_methods);
}
