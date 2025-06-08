from PIL import ImageFilter, ImageEnhance

#create draw on canvas tools
class DrawTools:
    def __init__(self,canvas, colour, size = 5):
        self.canvas = canvas
        self.colour = colour
        self.size = size

    def set_colour(self, new_colour):
        self.colour = new_colour

class BrushTool(DrawTools):
    def use_tool(self, event):
        x1, y1, x2, y2 = (event.x - 3), (event.y - 3), (event.x + 3), (event.y + 3)
        self.canvas.create_line(x1, y1, x2, y2,fill = self.colour)
class OvalTool(DrawTools):
    def use_tool(self,event):
        x,y = event.x, event.y
        r = self.size
        self.canvas.create_oval(x-r,y-r,x+r,y+r, fill = self.colour)

#create class for tools which based on pillow library
class PillowTools:
    def __init__(self, image):
        self.image = image

class BlurTool(PillowTools):
    def __init__(self, image, radius):
        self.image = image
        self.radius = radius

    def use_tool(self):
        return self.image.filter(ImageFilter.GaussianBlur(self.radius))

class ContrastTool(PillowTools):
    def __init__(self, image, factor):
        self.image = image
        self.factor = factor

    def use_tool(self):
        enhancer = ImageEnhance.Contrast(self.image)
        return enhancer.enhance(self.factor)

