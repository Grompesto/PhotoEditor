from PIL import Image, ImageDraw
from tools import BrushTool, TextTool, BlurTool, ContrastTool, RotateTool
import tkinter.simpledialog

class DummyCanvas:
    def move(self, *args, **kwargs):
        pass

class DummyEvent:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class DummyCallback:
    def __call__(self):
        pass

def test_brush_tool():
    image = Image.new("RGB", (100, 100), "white")
    original = image.copy()
    canvas = DummyCanvas()
    tool = BrushTool(canvas, image, [0, 0], DummyCallback(), colour="black", size=5)
    event = DummyEvent(50, 50)
    tool.use_tool(event)

    assert list(image.getdata()) != list(original.getdata()), "BrushTool failed"

def test_blur_tool():
    image = Image.new("RGB", (100, 100), "white")
    image.paste("black", [40, 40, 60, 60])
    original = image.copy()
    tool = BlurTool(image, radius=5)
    result = tool.use_tool()

    assert list(result.getdata()) != list(original.getdata()), "BlurTool failed"

def test_contrast_tool():
    image = Image.new("RGB", (100, 100), "gray")
    draw = ImageDraw.Draw(image)
    draw.rectangle([25, 25, 75, 75], fill="black")
    original = image.copy()
    tool = ContrastTool(image, factor=2.0)
    result = tool.use_tool()

    assert list(result.getdata()) != list(original.getdata()), "ContrastTool failed"

def test_rotate_tool():
    image = Image.new("RGB", (100, 100), "white")
    tool = RotateTool(image, angle=45)
    result = tool.use_tool()

    assert result.size != image.size, "RotateTool failed"

def test_text_tool():
    image = Image.new("RGB", (100, 100), "white")
    original = image.copy()
    canvas = DummyCanvas()
    tool = TextTool(canvas, image, [0, 0], DummyCallback(), colour="black", font_size=20)
    tkinter.simpledialog.askstring = lambda *args, **kwargs: "Test"
    event = DummyEvent(10, 10)
    tool.use_tool(event)

    assert list(image.getdata()) != list(original.getdata()), "TextTool failed"

def test_polymorphism():
    image = Image.new("RGB", (100, 100), "white")
    canvas = DummyCanvas()
    tools = [
        BrushTool(canvas, image, [0, 0], DummyCallback(), colour="blue", size=5),
        BlurTool(image, radius=2),
        ContrastTool(image, factor=1.5),
        RotateTool(image, angle=90)
    ]
    for tool in tools:
        if hasattr(tool, "use_tool"):
            if isinstance(tool, BrushTool):
                tool.use_tool(DummyEvent(30, 30))
            else:
                image = tool.use_tool()

    assert image is not None, "Polymorphic use_tool calls failed"

if __name__ == "__main__":
    test_brush_tool()
    test_blur_tool()
    test_contrast_tool()
    test_rotate_tool()
    test_text_tool()
    test_polymorphism()
    print("All tests passed!")