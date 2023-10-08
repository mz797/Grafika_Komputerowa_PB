import tkinter as tk
from tkinter import ttk
import random

my_clicked_object=None
selected_shape = None
start_x, start_y = 0, 0


def resetVariables():
    var_line_start_x.set(0)
    var_line_start_y.set(0)
    var_line_end_x.set(0)
    var_line_end_y.set(0)
    var_rectangle_x_top.set(0)
    var_rectangle_y_top.set(0)
    var_rectangle_x_bottom.set(0)
    var_rectangle_y_bottom.set(0)
    var_circle_x.set(0)
    var_circle_y.set(0)
    var_circle_r.set(0)
    var_circle_button.set('Draw circle')
    var_line_button.set('Draw line')
    var_rectangle_button.set('Draw rectangle')

def addLine():
    global var_can_draw
    global my_clicked_object
    
    sx=var_line_start_x.get()
    sy=var_line_start_y.get()
    ex=var_line_end_x.get()
    ey=var_line_end_y.get()
        
    if(var_can_draw.get() and my_clicked_object!=None):
        new_coords = [sx,sy,ex,ey]
        canvas.coords(my_clicked_object, *new_coords)
        my_clicked_object=None
    else:    
        line = canvas.create_line((sx, sy, ex, ey), fill = 'blue',width=5)
        tag=random.randint(0,100000)
        canvas.itemconfig(line,tags=f"line-{tag}")
        canvas.tag_bind(f"line-{tag}","<Button-1>",lambda event:handleLineClick(event, line))
        
    resetVariables()
    
def handleLineClick(event,line):
    global my_clicked_object
    global var_can_draw
    print('var_can_draw',var_can_draw.get())
    if(var_can_draw.get()):
        my_clicked_object=line
        bbox=canvas.coords(line)
        var_line_start_x.set(bbox[0])
        var_line_start_y.set(bbox[1])
        var_line_end_x.set(bbox[2])
        var_line_end_y.set(bbox[3])
        var_line_button.set('Change line')

def addRectangle():
    global var_can_draw
    global my_clicked_object
    sx=var_rectangle_x_top.get()
    sy=var_rectangle_y_top.get()
    ex=var_rectangle_x_bottom.get()
    ey=var_rectangle_y_bottom.get()
        
    if(var_can_draw.get() and my_clicked_object!=None):
        new_coords = [sx,sy,ex,ey]
        canvas.coords(my_clicked_object, *new_coords)
        my_clicked_object=None
    else:
        rectangle=canvas.create_rectangle((sx, sy, ex, ey), fill = 'purple',width=3)
        tag=random.randint(0,100000)
        canvas.itemconfig(rectangle,tags=f"rectangle-{tag}")
        canvas.tag_bind(f"rectangle-{tag}","<Button-1>",lambda event:handleRectangleClick(event, rectangle))
    resetVariables()
    
def handleRectangleClick(event,line):
    global my_clicked_object
    global var_can_draw
    print('var_can_draw',var_can_draw.get())
    if(var_can_draw.get()):
        my_clicked_object=line
        bbox=canvas.coords(line)
        var_rectangle_x_top.set(bbox[0])
        var_rectangle_y_top.set(bbox[1])
        var_rectangle_x_bottom.set(bbox[2])
        var_rectangle_y_bottom.set(bbox[3])
        var_rectangle_button.set('Change rectangle')

def addCircle():
    global var_can_draw
    global my_clicked_object
    sx=var_circle_x.get()
    sy=var_circle_y.get()
    r=var_circle_r.get()
    
    if(var_can_draw.get() and my_clicked_object!=None):
        new_coords = [sx-r,sy-r,sx+r,sy+r]
        canvas.coords(my_clicked_object, *new_coords)
        my_clicked_object=None
    else:
        circle=canvas.create_oval(sx-r,sy-r,sx+r,sy+r,fill = 'green',width=3)
        tag=random.randint(0,100000)
        canvas.itemconfig(circle,tags=f"circle-{tag}")
        canvas.tag_bind(f"circle-{tag}","<Button-1>",lambda event:handleCircleClick(event, circle))
        
    resetVariables()
    
def handleCircleClick(event,line):
    global my_clicked_object
    global var_can_draw
    if(var_can_draw.get()):
        my_clicked_object=line
        bbox=canvas.coords(line)
        radius = abs(bbox[0]-bbox[2])/2
        print(radius)
        var_circle_x.set(bbox[0]+radius)
        var_circle_y.set(bbox[1]+radius)
        var_circle_r.set(radius)
        var_circle_button.set('Change circle')

def on_canvas_click(event):
    global selected_shape, start_x, start_y
    x = event.x
    y = event.y
    selected_shape = canvas.find_closest(x, y)  # Znajdujemy najbliższy obiekt na canvas
    start_x, start_y = x, y  # Zachowujemy początkową pozycję myszy

def on_canvas_drag(event):
    global selected_shape, start_x, start_y
    if selected_shape:
        x = event.x
        y = event.y
        canvas.move(selected_shape, x - start_x, y - start_y)  # Przesuwamy zaznaczony obiekt o różnicę pozycji myszy
        start_x, start_y = x, y  # Aktualizujemy pozycję myszy
        resetVariables()

def on_canvas_release(event):
    global selected_shape
    selected_shape = None

window=tk.Tk()
window.title("Zadanie 1 Magda Zaborowska")
window.geometry('1000x700')

label = ttk.Label(window,text='Shapes :D')
label.grid(row=0,columnspan=6)

window.columnconfigure(0)
window.columnconfigure(6, weight=2)
# window.rowconfigure(0)

var_can_draw=tk.IntVar()
can_draw=ttk.Checkbutton(window,text='Change position mode',variable=var_can_draw, onvalue=1, offvalue=0)
can_draw.grid(row=2, column=6)

### LINE ###
line_label=ttk.Label(text='Line:')
line_label.grid(row=2,column=0)

var_line_start_x = tk.IntVar()
line_start_x_label=ttk.Label(text='Start X')
line_start_x_label.grid(row=1,column=1)
line_start_x = ttk.Entry(window,textvariable=var_line_start_x)
line_start_x.grid(row=2,column=1)

var_line_start_y = tk.IntVar()
line_start_y_label=ttk.Label(text= 'Start Y')
line_start_y_label.grid(row=1,column=2)
line_start_y = ttk.Entry(window, textvariable=var_line_start_y)
line_start_y.grid(row=2, column=2)

var_line_end_x = tk.IntVar()
line_end_x_label=ttk.Label(text='End X')
line_end_x_label.grid(row=1,column=3)
line_end_x = ttk.Entry(window,textvariable=var_line_end_x )
line_end_x.grid(row=2, column=3)

var_line_end_y = tk.IntVar()
line_end_y_label=ttk.Label(text='End Y')
line_end_y_label.grid(row=1,column=4)
line_end_y = ttk.Entry(window , textvariable=var_line_end_y)
line_end_y.grid(row=2, column=4)

var_line_button=tk.StringVar()
var_line_button.set('Draw line')
line_button = ttk.Button(command=addLine,textvariable=var_line_button)
line_button.grid(row=2, column=5,sticky='ew')

### Rectangle ###
rectangle_label=ttk.Label(text='Rectangle:')
rectangle_label.grid(row=4,column=0)

var_rectangle_x_top = tk.IntVar()
rectangle_x_top_label=ttk.Label(text='Top X')
rectangle_x_top_label.grid(row=3,column=1)
rectangle_x_top = ttk.Entry(window, textvariable=var_rectangle_x_top)
rectangle_x_top.grid(row=4,column=1)

var_rectangle_y_top = tk.IntVar()
rectangle_y_top_label=ttk.Label(text='Top Y')
rectangle_y_top_label.grid(row=3,column=2)
rectangle_y_top = ttk.Entry(window,textvariable=var_rectangle_y_top)
rectangle_y_top.grid(row=4, column=2)

var_rectangle_x_bottom = tk.IntVar()
rectangle_x_bottom_label=ttk.Label(text='Bottom X')
rectangle_x_bottom_label.grid(row=3,column=3)
rectangle_x_bottom = ttk.Entry(window,textvariable=var_rectangle_x_bottom)
rectangle_x_bottom.grid(row=4, column=3)

var_rectangle_y_bottom = tk.IntVar()
rectangle_y_bottom_label=ttk.Label(text='Bottom Y')
rectangle_y_bottom_label.grid(row=3,column=4)
rectangle_y_bottom = ttk.Entry(window,textvariable=var_rectangle_y_bottom)
rectangle_y_bottom.grid(row=4, column=4)

var_rectangle_button=tk.StringVar()
var_rectangle_button.set('Draw rectangle')
rectangle_button = ttk.Button(textvariable=var_rectangle_button, command=addRectangle)
rectangle_button.grid(row=4, column=5,sticky='ew')


### Circle ###
circle_label=ttk.Label(text='Circle:')
circle_label.grid(row=6,column=0)

var_circle_x = tk.IntVar()
circle_center_x_label=ttk.Label(text='Center X')
circle_center_x_label.grid(row=5,column=1)
circle_center_x = ttk.Entry(window,textvariable=var_circle_x)
circle_center_x.grid(row=6,column=1)

var_circle_y = tk.IntVar()
circle_center_y_label=ttk.Label(text='Center Y')
circle_center_y_label.grid(row=5,column=2)
circle_center_y = ttk.Entry(window,textvariable=var_circle_y)
circle_center_y.grid(row=6, column=2)

var_circle_r=tk.IntVar()
circle_r_label=ttk.Label(text='Radius')
circle_r_label.grid(row=5,column=3)
circle_r = ttk.Entry(window, textvariable=var_circle_r)
circle_r.grid(row=6, column=3)

var_circle_button=tk.StringVar()
var_circle_button.set('Draw circle')
circle_button = ttk.Button(textvariable=var_circle_button,command=addCircle)
circle_button.grid(row=6, column=4,sticky='ew')

canvas=tk.Canvas(window, bg='white',height=500, width=900,relief=tk.RIDGE, bd=0)
canvas.grid(row=7,column=0,columnspan=7)

canvas.bind("<Button-1>", on_canvas_click)
canvas.bind("<B1-Motion>", on_canvas_drag)   # Przeciąganie
canvas.bind("<ButtonRelease-1>", on_canvas_release)





window.mainloop()