class DrawTools:
    def __init__(self,canvas, color="green", size = 5):
        self.canvas = canvas
        self.color = color
        self.size = size

    def draw_line(self, event):
        x1, y1, x2, y2 = (event.x - 3), (event.y - 3), (event.x + 3), (event.y + 3)
        self.canvas.create_line(x1, y1, x2, y2,)

    def draw_oval(self,event):
        x,y = event.x, event.y
        r = self.size
        self.canvas.create_oval(x-r,y-r,x+r,y+r)