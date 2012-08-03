import hotshot
import hotshot.stats
import pygame
import sys
import time

PROFILER_FILE     = "hotshot_mandel_stats"
SCREEN_RESOLUTION = (640, 480)

class Screen(object):
    def __init__(self, surface, width, height, left_cord=-2.0, top_cord=1.0, scale=0.5):
        self.surface   = surface
        self.width     = width
        self.height    = height
        self.left_cord = left_cord
        self.top_cord  = top_cord
        self.scale     = scale

    def each_pixel(self):
        for x in range(self.width):
            for y in range(self.height):
                yield x, y

    def rescale_and_center(self, scale_factor):
        height = 1/self.scale
        width  = 1.25/self.scale

        self.left_cord += width/2 * (1 - 1.0/scale_factor)
        self.top_cord  += height/2 * (1.0/scale_factor - 1)

        self.scale *= scale_factor

    def up(self):
        self.top_cord += 0.25/self.scale

    def down(self):
        self.top_cord -= 0.25/self.scale

    def right(self):
        self.left_cord += 0.25/self.scale

    def left(self):
        self.left_cord -= 0.25/self.scale

    def scale_string(self):
        if self.scale > 1:
            return "1:%.0f" % self.scale
        else:
            return "%.0f:1" % (1.0/self.scale)

#
# Try to use a C version first.
#
# On my Athlon X2 4800+ generation of 1024x768 image with 100 iterations takes
# ~40 seconds using straight Python code and ~3 seconds using the C extension.
#
try:
    from _mandelbrot import color_for_pixel
except ImportError:
    def in_mandelbrot_set(point, max_iterations):
        "Return certainty that the given point intersects the Mandelbrot set."
        x, y = cx, cy = point

        for iteration in range(max_iterations):
            x, y = (x**2 - y**2 + cx) , (2*x*y + cy)
            if x**2 + y**2 > 4:
                break

        return iteration / float(max_iterations)

    def pixel_to_point(pixel, screen):
        "Convert pixel position to point coordinates."
        x, y = pixel
        return (1.25/screen.scale*x/(screen.width-1) + screen.left_cord,
                1.0/screen.scale*y/(screen.height-1) - screen.top_cord)

    def make_color(certainty):
        shade = int(255 * certainty)
        return tuple([shade]*3)

    def color_for_pixel(pixel, max_iterations, screen):
        point     = pixel_to_point(pixel, screen)
        certainty = in_mandelbrot_set(point, max_iterations)
        return make_color(certainty)

def draw(screen, max_iterations):
    for pixel in screen.each_pixel():
        color = color_for_pixel(pixel, max_iterations, screen)
        screen.surface.set_at(pixel, color)

def draw_and_flip(screen, max_iterations):
    print "Redrawing in scale %s (iterations: %d)..." % (screen.scale_string(), max_iterations)
    sys.stdout.flush()

    start = time.time()
    draw(screen, max_iterations)
    end = time.time()

    pygame.display.flip()

    print "done in %.02f seconds." % (end - start)

def setup_screen():
    pygame.init()
    window  = pygame.display.set_mode(SCREEN_RESOLUTION)
    surface = pygame.display.get_surface()

    return Screen(surface, *SCREEN_RESOLUTION)

def main():
    print "Scale with + and -. Move with arrows."

    redraw = False
    max_iterations = 100

    screen = setup_screen()
    draw_and_flip(screen, max_iterations)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE, pygame.K_q]:
                    return
                elif event.key in [pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS]:
                    screen.rescale_and_center(2)
                    max_iterations += 50
                    redraw = True
                elif event.key in [pygame.K_MINUS, pygame.K_KP_MINUS]:
                    if screen.scale < 0.5:
                        continue
                    screen.rescale_and_center(0.5)
                    max_iterations -= 50
                    redraw = True
                elif event.key == pygame.K_UP:
                    screen.up()
                    redraw = True
                elif event.key == pygame.K_DOWN:
                    screen.down()
                    redraw = True
                elif event.key == pygame.K_LEFT:
                    screen.left()
                    redraw = True
                elif event.key == pygame.K_RIGHT:
                    screen.right()
                    redraw = True

        if redraw:
            draw_and_flip(screen, max_iterations)
            redraw = False
        else:
            time.sleep(0.1)

def profile():
    screen = setup_screen()

    prof = hotshot.Profile(PROFILER_FILE)
    prof.runcall(draw_and_flip, screen, 1000)
    prof.close()

    stats = hotshot.stats.load(PROFILER_FILE)
    stats.sort_stats("time", "calls")
    stats.print_stats(20)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "prof":
        profile()
    else:
        main()
