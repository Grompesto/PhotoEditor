from PIL import ImageFilter, ImageEnhance, ImageDraw, ImageFont
from tkinter.simpledialog import askstring

#create draw on canvas tools
class DrawTools:
    def __init__(self, canvas, image_ref, image_pos, update_image_callback, colour, size=1):
        self.canvas = canvas
        self.colour = colour
        self.size = size
        self.image_ref = image_ref
        self.image_pos = image_pos
        self.update_image_callback = update_image_callback

    def set_colour(self, new_colour):
        self.colour = new_colour

    def set_size(self, new_size):
        self.size = new_size

class BrushTool(DrawTools):
    def use_tool(self, event):
        x, y = event.x - self.image_pos[0], event.y - self.image_pos[1]
        r = self.size
        draw = ImageDraw.Draw(self.image_ref)
        draw.ellipse((x - r, y - r, x + r, y + r), fill=self.colour)
        self.update_image_callback()

class OvalTool(DrawTools):
    def use_tool(self,event):
        x, y = event.x - self.image_pos[0], event.y - self.image_pos[1]
        r = self.size
        draw = ImageDraw.Draw(self.image_ref)
        draw.ellipse((x - r, y - r, x + r, y + r), fill=self.colour)
        self.update_image_callback()

#create classes for tools which based on pillow library
class PillowTools:
    def __init__(self, image):
        self.image = image

#create blur tool
class BlurTool(PillowTools):
    def __init__(self, image, radius):
        self.image = image
        self.radius = radius

    def use_tool(self):
        return self.image.filter(ImageFilter.GaussianBlur(self.radius))

#create contrast tool
class ContrastTool(PillowTools):
    def __init__(self, image, factor):
        self.image = image
        self.factor = factor

    def use_tool(self):
        enhancer = ImageEnhance.Contrast(self.image)
        return enhancer.enhance(self.factor)

#create move tool
class MoveTool:
    def __init__(self, canvas, image_id, image_pos):
        self.canvas = canvas
        self.image_id = image_id
        self.image_pos = image_pos
        self.start_x = 0
        self.start_y = 0

    def start_move(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def move_image(self, event):
        dx = event.x - self.start_x
        dy = event.y - self.start_y
        self.canvas.move(self.image_id, dx, dy)
        self.start_x = event.x
        self.start_y = event.y
        self.image_pos[0] += dx
        self.image_pos[1] += dy

#create rotate tool
class RotateTool:
    def __init__(self, image, angle):
        self.image = image
        self.angle = angle

    def use_tool(self):
        return self.image.rotate(self.angle, expand=True, fillcolor=('lightgray'))

#create text tool
class TextTool:
    def __init__(self, canvas, image_ref, image_pos, update_image_callback, colour='black', font_path=None, font_size=24):
        self.canvas = canvas
        self.image_ref = image_ref
        self.image_pos = image_pos
        self.update_image_callback = update_image_callback
        self.colour = colour
        self.font_size = font_size
        self.font_path = font_path or "arial.ttf"

    def set_colour(self, new_colour):
        self.colour = new_colour

    def use_tool(self, event):
        text = askstring("Input text", "Input text on the image:")
        draw = ImageDraw.Draw(self.image_ref)
        font = ImageFont.truetype(self.font_path, self.font_size)
        x = event.x - self.image_pos[0]
        y = event.y - self.image_pos[1]
        draw.text((x, y), text, font=font, fill=self.colour)
        self.update_image_callback()