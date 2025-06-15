from tkinter import *
from tkinter import filedialog, Scale, HORIZONTAL, messagebox
from PIL import ImageTk, Image
from tools import OvalTool, BrushTool, BlurTool, ContrastTool, MoveTool, RotateTool, TextTool

#create main window
window = Tk()
window.title("PRB (Photoshop's retarded brother)")
window.geometry('1920x1080')
window.resizable(width=True,height=True)
icon = PhotoImage(file ='/assets/Retarded brother.png')
window.iconphoto(True,icon)

#create main left frame for smaller frames
left_frame = Frame(window, bg="darkgray")
left_frame.grid(row=0, column=0, rowspan=2, sticky="ns")

#create frame with tools
tool_bar = Frame(left_frame, bg = 'gray',borderwidth=10)
tool_bar.pack(side=TOP)

tool_text = Button(tool_bar,text='Text')
tool_text.pack()
tool_oval = Button(tool_bar,text='Oval')
tool_oval.pack()
tool_brush = Button(tool_bar,text='Brush')
tool_brush.pack()
tool_move = Button(tool_bar,text='Move')
tool_move.pack()
tool_contrast = Button(tool_bar,text='Contrast')
tool_contrast.pack()
tool_blur = Button(tool_bar,text='Blur')
tool_blur.pack()
tool_rotate = Button(tool_bar,text='Rotate')
tool_rotate.pack()

#create color palette frame
colorpalette_bar = Frame(left_frame,bg='gray',borderwidth=10)
colorpalette_bar.pack(side=BOTTOM)

color_green = Button(colorpalette_bar, bg='green',command=lambda: select_colour('green'))
color_green.pack()
color_blue = Button(colorpalette_bar, bg='blue',command=lambda: select_colour('blue'))
color_blue.pack()
color_red = Button(colorpalette_bar, bg='red',command=lambda: select_colour('red'))
color_red.pack()
color_yellow = Button(colorpalette_bar, bg='yellow',command=lambda: select_colour('yellow'))
color_yellow.pack()
color_purple = Button(colorpalette_bar, bg='purple',command=lambda: select_colour('purple'))
color_purple.pack()
color_black = Button(colorpalette_bar, bg='black',command=lambda: select_colour('black'))
color_black.pack()
color_orange = Button(colorpalette_bar, bg='orange',command=lambda: select_colour('orange'))
color_orange.pack()

#area for image
canvas = Canvas(window, width=1280, height=720, bg = 'lightgray')
canvas.grid(row=0,column=1)

current_image = None
tk_image = None
image_id = None
image_pos = [0, 0]

#lists for history of changes of image
history = []
redo_history = []

#create frame for scale grid
right_frame = Frame(window, bg="darkgray", borderwidth=10)
right_frame.grid(row=0, column=2, rowspan=2, sticky="ns")

#scale for rotate
rotate_scale = Scale(right_frame, from_=-180, to=180, orient=HORIZONTAL, label="Rotate angle")
rotate_scale.set(0)
rotate_scale.pack(pady=20, padx=10, fill="x")

#scale for blur
blur_scale = Scale(right_frame, from_=1, to=20, orient=HORIZONTAL, label="Blur radius")
blur_scale.set(0)
blur_scale.pack(pady=20, padx=10, fill="x")

#scale for contrast
contrast_scale = Scale(right_frame, from_=0.1, to=5.0, resolution=0.1, orient=HORIZONTAL, label="Contrast factor")
contrast_scale.set(0)
contrast_scale.pack(pady=20, padx=10, fill="x")

#scale for tools size
tool_size_scale = Scale(right_frame, from_=1, to=100, orient=HORIZONTAL, label="Tool size", command=lambda val: select_size(int(val)))
tool_size_scale.set(24)
tool_size_scale.pack(pady=20, padx=10, fill="x")

#function to load image through menubar->file->open...
def image_open():
    global current_image, tk_image, image_id, image_pos
    file_types = [('Image Files','*.png;*.jpg;*.jpeg')]
    path = filedialog.askopenfilename(filetypes=file_types)
    current_image = Image.open(path).resize((700,700))
    tk_image = ImageTk.PhotoImage(current_image)
    canvas.delete("all")
    image_pos = [0, 0]
    image_id = canvas.create_image(image_pos[0], image_pos[1], anchor=NW, image=tk_image)
#error message if image isn't loaded
def show_error():
    messagebox.showwarning("No image", "Please load an image.")

#function to save image through menubar->file->save as...
def image_save_as():
    if current_image is None:
        return
    file_types = [('Image Files', '*.png;*.jpg;*.jpeg')]
    path = filedialog.asksaveasfilename(filetypes=file_types)
    current_image.save(path)

#function to update image after operations
def update_image():
    global tk_image, image_id
    tk_image = ImageTk.PhotoImage(current_image)
    canvas.delete(image_id)
    image_id = canvas.create_image(image_pos[0], image_pos[1], anchor=NW, image=tk_image)

#function for blank file through menubar->file->new file
def new_file():
    global current_image, tk_image, image_id, history, redo_history
    canvas.delete("all")
    current_image = None
    tk_image = None
    image_id = None
    history.clear()
    redo_history.clear()

#function to make step forward
def stepf():
    global current_image, tk_image, history, redo_history, image_id, image_pos
    if redo_history:
        history.append(current_image.copy())
        current_image = redo_history.pop()
        tk_image = ImageTk.PhotoImage(current_image)
        canvas.delete(image_id)
        image_id = canvas.create_image(image_pos[0], image_pos[1], anchor=NW, image=tk_image)

#function to make step backward
def stepb():
    global current_image, tk_image, history, redo_history, image_id, image_pos
    if history:
        redo_history.append(current_image.copy())
        current_image = history.pop()
        tk_image = ImageTk.PhotoImage(current_image)
        canvas.delete(image_id)
        image_id = canvas.create_image(image_pos[0], image_pos[1], anchor=NW, image=tk_image)

#allows to select colour
colour = 'black'
def select_colour(new_colour):
    global colour
    colour = new_colour
    if current_tool is not None:
        current_tool.set_colour(colour)

#allows to select size for draw tools
size = 1
def select_size(new_size):
    global size
    size = new_size
    if current_tool is not None:
        current_tool.set_size(size)

#allows to select tools
current_tool = None
active_button = None

#function to deselect tool
def deselect_tool():
    global active_button, current_tool
    if active_button:
        canvas.unbind(active_button)
    active_button = None
    current_tool = None

#function for brush tool
def select_brush():
    global current_tool, active_button
    deselect_tool()
    if not current_image:
        show_error()
        return
    history.append(current_image.copy())
    redo_history.clear()
    current_tool = BrushTool(canvas, current_image, image_pos, update_image, colour, size)
    canvas.bind('<B1-Motion>', current_tool.use_tool)
    active_button = '<B1-Motion>'

#function for oval tool
def select_oval():
    global current_tool, active_button
    deselect_tool()
    if not current_image:
        show_error()
        return
    history.append(current_image.copy())
    redo_history.clear()
    current_tool = OvalTool(canvas, current_image, image_pos, update_image, colour, size)
    canvas.bind('<Button-1>', current_tool.use_tool)
    active_button = '<Button-1>'

#function for move tool
def select_move():
    global current_tool, active_button,image_id, image_pos
    deselect_tool()
    if not current_image:
        show_error()
        return
    current_tool = MoveTool(canvas, image_id, image_pos)
    canvas.bind('<Button-1>', current_tool.start_move)
    canvas.bind('<B1-Motion>', current_tool.move_image)
    active_button = '<B1-Motion>'

#function for rotate tool
def select_rotate():
    global current_image, tk_image, history, redo_history, image_id, image_pos
    if not current_image:
        show_error()
        return
    history.append(current_image.copy())
    redo_history.clear()
    angle = rotate_scale.get()
    rotate_tool = RotateTool(current_image, angle)
    current_image = rotate_tool.use_tool()
    tk_image = ImageTk.PhotoImage(current_image)
    canvas.delete(image_id)
    image_id = canvas.create_image(image_pos[0], image_pos[1], anchor=NW, image=tk_image)

#function for blur tool
def select_blur():
    global current_image, tk_image, history, redo_history, image_id, image_pos
    if not current_image:
        show_error()
        return
    history.append(current_image.copy())
    redo_history.clear()
    radius = blur_scale.get()
    blur_tool = BlurTool(current_image, radius)
    current_image = blur_tool.use_tool()
    tk_image = ImageTk.PhotoImage(current_image)
    canvas.delete(image_id)
    image_id = canvas.create_image(image_pos[0], image_pos[1], anchor=NW, image=tk_image)

#function for contrast tool
def select_contrast():
    global current_image, tk_image, history, redo_history, image_id, image_pos
    if not current_image:
        show_error()
        return
    history.append(current_image.copy())
    redo_history.clear()
    factor = contrast_scale.get()
    contrast_tool = ContrastTool(current_image, factor)
    current_image = contrast_tool.use_tool()
    tk_image = ImageTk.PhotoImage(current_image)
    canvas.delete(image_id)
    image_id = canvas.create_image(image_pos[0], image_pos[1], anchor=NW, image=tk_image)

#function for text tool
def select_text():
    global current_tool, active_button
    deselect_tool()
    if not current_image:
        show_error()
        return
    history.append(current_image.copy())
    redo_history.clear()
    font_size = tool_size_scale.get()
    current_tool = TextTool(canvas, current_image, image_pos, update_image, colour, font_size=font_size)
    canvas.bind('<Button-1>', current_tool.use_tool)
    active_button = '<Button-1>'

# create menu bar
menubar = Menu(window)
file = Menu(menubar,tearoff=0)
edit = Menu(menubar,tearoff=0)
rightClick = Menu(window, tearoff=0)

menubar.add_cascade(label = 'File', menu = file)
menubar.add_cascade(label = 'Edit', menu = edit)

file.add_command(label='New file', command=new_file)
file.add_command(label='Open...', command=image_open)
file.add_command(label='Save...', command=image_save_as)
file.add_command(label='Save as...', command=image_save_as)
file.add_separator()
file.add_command(label='Exit', command=window.quit)

edit.add_command(label='Step Forward', command=stepf)
edit.add_command(label='Step Backward',command=stepb)

tool_blur.config(command=select_blur)
tool_contrast.config(command=select_contrast)
tool_oval.config(command=select_oval)
tool_brush.config(command=select_brush)
tool_move.config(command=select_move)
tool_rotate.config(command=select_rotate)
tool_text.config(command=select_text)

window.config(menu = menubar)

window.mainloop()