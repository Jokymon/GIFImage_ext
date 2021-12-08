import pygame
import time
from PIL import Image


class AnimatedGifSprite(pygame.sprite.Sprite):
    """A Sprite-derived class that handles animation of animated GIFs"""
    def __init__(self, position, filename):
        """Construct a new AnimatedGifSprite object.

        By default playback of the animation is active and with every call to
        the :func:`update`-function the correct next frame is selected.

        :param tuple position: A tuple with two elements specifying the x and y 
            coordinates where the sprite will be placed
        :param string filename: Path to an animated GIF file"""
        super().__init__()

        self.filename = filename
        self.playback_speed = 1
        self.scaling_factor = 1
        self.frames = self.get_frames(filename)

        self.cur = 0
        self.ptime = time.time()

        self.running = True
        self.breakpoint = len(self.frames)-1
        self.startpoint = 0
        self.reversed = False

        self.image = self.frames[0][0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position


    def get_frames(self, filename):
        image = Image.open(filename) 
        pal = image.getpalette()
        base_palette = []
        for i in range(0, len(pal), 3):
            rgb = pal[i:i+3]
            base_palette.append(rgb)

        all_tiles = []
        try:
            while 1:
                if not image.tile:
                    image.seek(0)
                if image.tile:
                    all_tiles.append(image.tile[0][3][0])
                image.seek(image.tell()+1)
        except EOFError:
            image.seek(0)

        all_tiles = tuple(set(all_tiles))

        frames = []
        try:
            while 1:
                try:
                    duration = image.info["duration"]
                except:
                    duration = 100

                duration *= .001 #convert to milliseconds!
                
                duration *= self.playback_speed
                
                cons = False

                x0, y0, x1, y1 = (0, 0) + image.size
                if image.tile:
                    tile = image.tile
                else:
                    image.seek(0)
                    tile = image.tile
                if len(tile) > 0:
                    x0, y0, x1, y1 = tile[0][1]

                if all_tiles:
                    if all_tiles in ((6,), (7,)):
                        cons = True
                        pal = image.getpalette()
                        palette = []
                        for i in range(0, len(pal), 3):
                            rgb = pal[i:i+3]
                            palette.append(rgb)
                    elif all_tiles in ((7, 8), (8, 7)):
                        pal = image.getpalette()
                        palette = []
                        for i in range(0, len(pal), 3):
                            rgb = pal[i:i+3]
                            palette.append(rgb)
                    else:
                        palette = base_palette
                else:
                    palette = base_palette

                pi = pygame.image.fromstring(image.tobytes(), image.size, image.mode)
                pi.set_palette(palette)
                if "transparency" in image.info:
                    pi.set_colorkey(image.info["transparency"])
                pi2 = pygame.Surface(image.size, pygame.SRCALPHA)
                if cons:
                    for i in frames:
                        pi2.blit(i[0], (0,0))
                pi2.blit(pi, (x0, y0), (x0, y0, x1-x0, y1-y0))

                frames.append([pi2, duration])
                image.seek(image.tell()+1)
        except EOFError:
            pass
        return frames

    def update(self, *args, **kwargs):
        """This function needs to be called once for every frame to actually see any animation.

        The function signature is written such that :class:`AnimatedGifSprite` objects can be
        added to a :class:`pygame.sprite.Group` and :func:`update` can be called on the group with
        any parameters useful for other objects in that group without crashing the
        :class:`AnimatedGifSprite`-objects. The class :class:`AnimatedGifSprite` does not need any
        parameters for the call to :func:`update`."""
        if self.running:
            if time.time() - self.ptime > self.frames[self.cur][1]:
                if self.reversed:
                    self.cur -= 1
                    if self.cur < self.startpoint:
                        self.cur = self.breakpoint
                else:
                    self.cur += 1
                    if self.cur > self.breakpoint:
                        self.cur = self.startpoint

                self.ptime = time.time()
        if self.scaling_factor == 1:
            self.image = self.frames[self.cur][0]
        else:
            self.image = pygame.transform.scale(self.frames[self.cur][0],
                                (int(self.rect.width * self.scaling_factor),
                                 int(self.rect.height * self.scaling_factor)))

    def seek(self, num):
        """Directly jump to the frame with the given numbers.

        :param int num: The frame number to jump to. Frame numbers outside the
            available frame number count will be capped to be inside the valid
            range.
        """
        self.cur = num
        if self.cur < 0:
            self.cur = 0
        if self.cur >= len(self.frames):
            self.cur = len(self.frames)-1

    def set_bounds(self, start, end):
        if start < 0:
            start = 0
        if start >= len(self.frames):
            start = len(self.frames) - 1
        if end < 0:
            end = 0
        if end >= len(self.frames):
            end = len(self.frames) - 1
        if end < start:
            end = start
        self.startpoint = start
        self.breakpoint = end

    def play(self):
        """Start playback of the animation."""
        self.running = True

    def pause(self):
        """Stop playback of the animation."""
        self.running = False

    def next_frame(self):
        """Step to next frame in the animation.

        When this function is called while the animation is playing, the
        playback is stopped.

        Once the last frame is reached, frames are wrapped around and the
        next frame from the start is shown again."""
        if self.running:
            self.pause()
        else:
            self.cur += 1
            if self.cur > self.breakpoint:
                self.cur = self.startpoint

    def prev_frame(self):
        """Step to previous frame in the animation.

        When this function is called while the animation is playing, the
        playback is stopped.

        Once the first frame is reached, frames are wrapped around and the
        next frame from the end is shown."""
        if self.running:
            self.pause()
        else:
            self.cur -= 1
            if self.cur < 0:
                self.cur = self.breakpoint

    def slow_down(self):
        self.playback_speed += .05 if self.playback_speed != .01 else .04
        self.get_frames()
        self.seek(self.cur)
        
    def speed_up(self):
        if self.playback_speed - .05 <= 0:
            self.playback_speed = .01
        else:
            self.playback_speed -= .25
        self.get_frames()
        self.seek(self.cur)

    def scale(self, scale_factor):
        """Scale the animation by the given scaling factor.

        :param double scale_factor The factor by which all the frame of the
            animation are scaled."""
        self.scaling_factor = scale_factor

    def reset_scale(self):
        """Reset the scaling factor to 1.0"""
        self.scaling_factor = 1

    def rewind(self):
        self.seek(0)
    def fastforward(self):
        self.seek(self.length()-1)

    def get_height(self):
        return self.image.size[1]
    def get_width(self):
        return self.image.size[0]
    def get_size(self):
        return self.image.size
    def length(self):
        return len(self.frames)
    def reverse(self):
        self.reversed = not self.reversed
    def reset(self):
        self.cur = 0
        self.ptime = time.time()
        self.reversed = False
