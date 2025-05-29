class DrawTools:
    def __init__(self,canvas, colour, size = 5):
        self.canvas = canvas
        self.colour = colour
        self.size = size

    def set_colour(self, new_colour):
        self.colour = new_colour

    def draw_line(self, event):
        x1, y1, x2, y2 = (event.x - 3), (event.y - 3), (event.x + 3), (event.y + 3)
        self.canvas.create_line(x1, y1, x2, y2,fill = self.colour)
    def draw_oval(self,event):
        x,y = event.x, event.y
        r = self.size
        self.canvas.create_oval(x-r,y-r,x+r,y+r, fill = self.colour)
