CC     = gcc
CFLAGS = $(shell pkg-config --cflags sdl2)
LDFLAGS = -lSDL

render_scene: render_scene.c
	$(CC) $(CFLAGS) -o render_scene render_scene.c $(LDFLAGS)

run: render_scene
	SDL_VIDEODRIVER=offscreen ./render_scene

clean:
	rm -f render_scene scene.bmp
