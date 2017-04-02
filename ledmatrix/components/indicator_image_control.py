class Indicator_Image_Control(object):
    """ Handle update logic for animations """

    def update(self, indicator_image):
        pass

class Image_Pause_Control(Indicator_Image_Control):
    """ Handle pauses """

    def __init__(self, frames):

        self.frames = frames
        self._current_frame = 0

    def update(self, image):

        self._current_frame += 1

        if self._current_frame > self.frames:
            raise StopIteration

class Image_ScrollDown_Control(Indicator_Image_Control):
    """ Scroll the image down """

    def update(self, image):

        image.move_down() # Will return StopIteration

class Image_FadeIn_Control(Indicator_Image_Control):
    """ Gently fade in """

    def __init__(self, max_brightness=1.0, step=0.01):

        self.max_brightness = max_brightness
        self.step = step

    def update(self, image):

        image.brightness += self.step

        if image.brightness > self.max_brightness:
            raise StopIteration

class Image_FadeOut_Control(Indicator_Image_Control):
    """ Gently fade out """

    def __init__(self, min_brightness=0.0, step=-0.01):

        self.min_brightness = min_brightness
        self.step = step

    def update(self, image):

        image.brightness += self.step

        if image.brightness < self.min_brightness:
            raise StopIteration

class Image_ScrollLeft_Control(Indicator_Image_Control):

    def update(self, image):

        image.next() # can throw StopIteration
