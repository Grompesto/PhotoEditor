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