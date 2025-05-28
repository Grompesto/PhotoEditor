from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image

#create main window
window = Tk()
window.title("PRB (Photoshop's retarded brother)")
window.geometry('1280x720')
window.resizable(width=False,height=False)

# icon for text tool
imagetext = Image.open("C:/Users/zlaya/PycharmProjects/PythonProject/assets/free-icon-text-2266755.png").resize((25,25))
image_text = ImageTk.PhotoImage(imagetext)


# create frame with tools
tool_bar = Frame(window, bg = 'gray',borderwidth=10)

tool_text = Button(tool_bar,image=image_text).pack()
tool_line = Button(tool_bar,text='/').pack()
tool_selection = Button(tool_bar,text='H').pack()
tool_lupa = Button(tool_bar,text='O').pack()
tool_slice = Button(tool_bar,text='S').pack()
tool_brash = Button(tool_bar,text='B').pack()
tool_move = Button(tool_bar,text='M').pack()
tool_erasor = Button(tool_bar,text='E').pack()
tool_marquee = Button(tool_bar,text='Q').pack()
tool_eyedropper = Button(tool_bar,text='Y').pack()
tool_gradient = Button(tool_bar,text='G').pack()
tool_blur = Button(tool_bar,text='U').pack()
tool_rotate = Button(tool_bar,text='R').pack()
tool_hand = Button(tool_bar,text='D').pack()
tool_bar.grid(row=0,column=0)

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

edit.add_command(label='Undo move')
edit.add_command(label='Step Forward')
edit.add_command(label='Step Backward')
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


window.bind('<Button-3>',right_popup)

window.config(menu = menubar)

window.mainloop()