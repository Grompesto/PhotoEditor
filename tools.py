from PIL import ImageFilter, ImageEnhance, ImageDraw, ImageFont
from tkinter.simpledialog import askstring

class Tools:
    def __init__(self, canvas, image_ref, image_pos, update_image_callback):
        self._canvas = canvas
        self._image_ref = image_ref
        self._image_pos = image_pos
        self._update_image = update_image_callback

#create classes for drawing on canvas tools
class DrawTools(Tools):
    def __init__(self, canvas, image_ref, image_pos, update_image_callback, colour, size=1):
        super().__init__(canvas, image_ref, image_pos, update_image_callback)
        self.colour = colour
        self.size = size

    def set_colour(self, new_colour):
        self.colour = new_colour

    def set_size(self, new_size):
        self.size = new_size

#create text tool
class TextTool(DrawTools):
    def __init__(self, canvas, image_ref, image_pos, update_image_callback, colour='black', font_path=None, font_size=24):
        super().__init__(canvas, image_ref, image_pos, update_image_callback, colour, font_size)
        self.font_path = font_path or "arial.ttf"
        self.font_size = font_size

    def set_colour(self, new_colour):
        self.colour = new_colour

    def set_size(self, new_size):
        self.font_size = new_size

    def use_tool(self, event):
        text = askstring("Input text", "Input text on the image:")
        draw = ImageDraw.Draw(self._image_ref)
        font = ImageFont.truetype(self.font_path, self.font_size)
        x = event.x - self._image_pos[0]
        y = event.y - self._image_pos[1]
        draw.text((x, y), text, font=font, fill=self.colour)
        self._update_image()

#create brush tool
class BrushTool(DrawTools):
    def use_tool(self, event):
        x, y = event.x - self._image_pos[0], event.y - self._image_pos[1]
        r = self.size
        draw = ImageDraw.Draw(self._image_ref)
        draw.ellipse((x - r, y - r, x + r, y + r), fill=self.colour)
        self._update_image()

#create oval tool
class OvalTool(DrawTools):
    def use_tool(self,event):
        x, y = event.x - self._image_pos[0], event.y - self._image_pos[1]
        r = self.size
        draw = ImageDraw.Draw(self._image_ref)
        draw.ellipse((x - r, y - r, x + r, y + r), fill=self.colour)
        self._update_image()

#create classes for tools which based on pillow library
class PillowTools:
    def __init__(self, image):
        self._image = image

#create blur tool
class BlurTool(PillowTools):
    def __init__(self, image, radius):
        super().__init__(image)
        self._radius = radius

    def use_tool(self):
        return self._image.filter(ImageFilter.GaussianBlur(self._radius))

#create contrast tool
class ContrastTool(PillowTools):
    def __init__(self, image, factor):
        super().__init__(image)
        self._factor = factor

    def use_tool(self):
        enhancer = ImageEnhance.Contrast(self._image)
        return enhancer.enhance(self._factor)

#create move tool
class MoveTool:
    def __init__(self, canvas, image_id, image_pos):
        self._canvas = canvas
        self._image_id = image_id
        self._image_pos = image_pos
        self._start_x = 0
        self._start_y = 0

    def start_move(self, event):
        self._start_x = event.x
        self._start_y = event.y

    def move_image(self, event):
        dx = event.x - self._start_x
        dy = event.y - self._start_y
        self._canvas.move(self._image_id, dx, dy)
        self._start_x = event.x
        self._start_y = event.y
        self._image_pos[0] += dx
        self._image_pos[1] += dy

#create rotate tool
class RotateTool(PillowTools):
    def __init__(self, image, angle):
        super().__init__(image)
        self._angle = angle

    def use_tool(self):
        return self._image.rotate(self._angle, expand=True, fillcolor='lightgray')