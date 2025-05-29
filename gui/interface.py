from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
from editor.tools import DrawTools


#create main window
window = Tk()
window.title("PRB (Photoshop's retarded brother)")
window.geometry('1280x720')
window.resizable(width=False,height=False)
icon = PhotoImage(file ='C:/Users/zlaya/PycharmProjects/PythonProject/assets/Retarded brother.png')
window.iconphoto(True,icon)

# icon for text tool
imagetext = Image.open("C:/Users/zlaya/PycharmProjects/PythonProject/assets/free-icon-text-2266755.png").resize((25,25))
image_text = ImageTk.PhotoImage(imagetext)

#create main left frame for smaller frames
left_frame = Frame(window, bg="darkgray")
left_frame.grid(row=0, column=0, rowspan=2, sticky="ns")

# create frame with tools
tool_bar = Frame(left_frame, bg = 'gray',borderwidth=10)
tool_bar.pack(side=TOP)

tool_text = Button(tool_bar,image=image_text)
tool_text.pack()
tool_line = Button(tool_bar,text='/')
tool_line.pack()
tool_selection = Button(tool_bar,text='H')
tool_selection.pack()
tool_lupa = Button(tool_bar,text='O')
tool_lupa.pack()
tool_slice = Button(tool_bar,text='S')
tool_slice.pack()
tool_brush = Button(tool_bar,text='B')
tool_brush.pack()
tool_move = Button(tool_bar,text='M')
tool_move.pack()
tool_erasor = Button(tool_bar,text='E')
tool_erasor.pack()
tool_marquee = Button(tool_bar,text='Q')
tool_marquee.pack()
tool_eyedropper = Button(tool_bar,text='Y')
tool_eyedropper.pack()
tool_gradient = Button(tool_bar,text='G')
tool_gradient.pack()
tool_blur = Button(tool_bar,text='U')
tool_blur.pack()
tool_rotate = Button(tool_bar,text='R')
tool_rotate.pack()
tool_hand = Button(tool_bar,text='D')
tool_hand.pack()

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

# area for image
canvas = Canvas(window, width=1280, height=720, bg = 'lightgray')
canvas.grid(row=0,column=1)
current_image = None
tk_image = None

# function to load image through menubar->file->open...
def image_open():
    global current_image, tk_image
    fileTypes = [('Image Files','*.png;*.jpg;*.jpeg')]
    path = filedialog.askopenfilename(filetypes=fileTypes)
    current_image = Image.open(path).resize((500,500))
    tk_image = ImageTk.PhotoImage(current_image)
    canvas.delete("all")
    canvas.create_image(0, 0, anchor=NW, image=tk_image)

# function to save image through menubar->file->save as...
def image_save_as():
    fileTypes = [('Image Files', '*.png;*.jpg;*.jpeg')]
    path = filedialog.asksaveasfilename(filetypes=fileTypes)
    current_image.save(path)

# function for blank file through menubar->file->new file
def new_file():
    canvas.delete("all")

def undo_move():
    None

def stepf():
    None

def stepb():
    None

#allows to select colour
colour = 'black'
def select_colour(new_colour):
    global colour
    colour = new_colour
    current_tool.set_colour(colour)

#allows to select tools
current_tool = None
active_button = None
def deselect_tool():
    global active_button
    canvas.unbind(active_button)
    active_button = None

def select_brush():
    global current_tool, active_button
    deselect_tool()
    current_tool = DrawTools(canvas, colour)
    canvas.bind('<B1-Motion>', current_tool.draw_line)
    active_button = '<B1-Motion>'

def select_oval():
    global current_tool, active_button
    deselect_tool()
    current_tool = DrawTools(canvas, colour)
    canvas.bind('<Button-1>', current_tool.draw_oval)
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
file.add_command(label='Save...')
file.add_command(label='Save as...', command=image_save_as)
file.add_separator()
file.add_command(label='Exit', command=window.quit)

edit.add_command(label='Undo move',command=undo_move)
edit.add_command(label='Step Forward', command=stepf)
edit.add_command(label='Step Backward',command=stepb)
edit.add_separator()
edit.add_command(label='Cut')
edit.add_command(label='Copy')
edit.add_command(label='Paste')

rightClick.add_command(label = 'Cut')
rightClick.add_command(label='Copy')
rightClick.add_command(label='Paste')

# add popup menu when right-clicked
def right_popup(event):
    rightClick.tk_popup(event.x_root, event.y_root)

tool_line.config(command=select_oval)
tool_brush.config(command=select_brush)
window.bind('<Button-3>',right_popup)

window.config(menu = menubar)

window.mainloop()