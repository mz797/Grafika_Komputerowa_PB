import math
import tkinter as tk
from tkinter import ttk
import random

my_clicked_object=None
selected_shape = None
start_x, start_y = 0, 0

is_drawing_line = False
is_drawing_rectangle=False
is_drawing_circle=False

is_changing_shape = False

def enable_shape_change():
    global is_changing_shape,var_change_shape_button
    is_changing_shape = True
    var_change_shape_button.set('Now you can change Shape')

def midpoint(x1, y1, x2, y2):
    return ((x1 + x2)/2, (y1 + y2)/2)

def save_coordinates():
    objects = canvas.find_all()
    data = []

    for obj in objects:
        if canvas.type(obj) == "rectangle":
            data.append(("rectangle", canvas.coords(obj)))
        elif canvas.type(obj) == "oval":
            data.append(("oval", canvas.coords(obj)))
        elif canvas.type(obj) == "line":
            data.append(("line", canvas.coords(obj)))

    with open("coordinates.txt", "w") as file:
        for item in data:
            file.write(f"{item[0]}: {item[1]}\n")
            
            
def read_coordinates():
    canvas.delete("all")

    try:
        with open("coordinates.txt", "r") as file:
            lines = file.readlines()

            for line in lines:
                tag=random.randint(0,100000)
                parts = line.strip().split(": ")
                if len(parts) == 2:
                    obj_type, coords_str = parts
                    coords = eval(coords_str)
                    if obj_type == "rectangle":
                        rectangle = canvas.create_rectangle(coords, fill="purple", width=3)
                        canvas.itemconfig(rectangle,tags=f"rectangle-{tag}")
                        canvas.tag_bind(f"rectangle-{tag}","<Button-1>",lambda event:handleRectangleClick(event, rectangle))
                    elif obj_type == "oval":
                        circle=canvas.create_oval(coords, fill="green", width=3)
                        canvas.itemconfig(circle,tags=f"circle-{tag}")
                        canvas.tag_bind(f"circle-{tag}","<Button-1>",lambda event:handleCircleClick(event, circle))
                    elif obj_type == "line":
                        line = canvas.create_line(coords, fill="blue", width=5)
                        canvas.itemconfig(line,tags=f"line-{tag}")
                        canvas.tag_bind(f"line-{tag}","<Button-1>",lambda event:handleLineClick(event, line))
    except FileNotFoundError:
        pass

def reset():
    canvas.delete("all")
    
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

def startDrawingLine():
    global is_drawing_line
    is_drawing_line = True
    var_draw_line_button.set('Draw line by mouse click and move')

# Funkcja do zakończenia rysowania linii
def endDrawingLine():
    global is_drawing_line
    is_drawing_line = False
    var_draw_line_button.set('Draw line')

def startDrawingRectangle():
    global is_drawing_rectangle
    is_drawing_rectangle=True
    var_draw_rectangle_button.set('Draw rectangle by mouse click and move')

def endDravingRectangle():
    global is_drawing_rectangle
    is_drawing_rectangle=False
    var_draw_rectangle_button.set('Draw rectangle')

def startDrawingCircle():
    global is_drawing_circle
    is_drawing_circle=True
    var_draw_circle_button.set('Draw circle by mouse click and move')
    
def endDravingCircle():
    global is_drawing_circle
    is_drawing_circle=False
    var_draw_circle_button.set('Draw circle')
    
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
    global my_clicked_object, var_can_draw
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
    
def handleRectangleClick(event,rectangle):
    global my_clicked_object
    global var_can_draw
    print('var_can_draw',var_can_draw.get())
    if(var_can_draw.get()):
        my_clicked_object=rectangle
        bbox=canvas.coords(rectangle)
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
    global selected_shape, start_x, start_y, is_changing_shape
    if is_drawing_line or is_drawing_rectangle or is_drawing_circle:
        start_x = event.x
        start_y = event.y
    elif is_changing_shape:
        x = event.x
        y = event.y
        selected_shape = canvas.find_closest(x, y)
        start_x, start_y = x, y
    else:
        x = event.x
        y = event.y
        selected_shape = canvas.find_closest(x, y)  # Znajdujemy najbliższy obiekt na canvas
        start_x, start_y = x, y  # Zachowujemy początkową pozycję myszy

def on_canvas_drag(event):
    global selected_shape, start_x, start_y,var_change_shape_button
    if selected_shape and not is_changing_shape:
        x = event.x
        y = event.y
        canvas.move(selected_shape, x - start_x, y - start_y)
        start_x, start_y = x, y
        resetVariables()
    elif selected_shape and is_changing_shape:
        x = event.x
        y = event.y
        if canvas.type(selected_shape) == "line":
            canvas.coords(selected_shape, start_x, start_y, x, y)
        elif canvas.type(selected_shape) == "rectangle":
            print(x,start_x)
            coords = canvas.coords(selected_shape)
            new_coords = [coords[0], coords[1], x, y]
            canvas.coords(selected_shape, *new_coords)
        elif canvas.type(selected_shape) == "oval":
            coords = canvas.coords(selected_shape)
            new_coords = [coords[0], coords[1], x, y]
            canvas.coords(selected_shape, *new_coords)
        var_change_shape_button.set('Change Shape')

def on_canvas_release(event):
    global selected_shape,is_changing_shape
    x = event.x
    y = event.y
    if is_changing_shape:
        selected_shape = None
        is_changing_shape = False
    elif is_drawing_line:
        line = canvas.create_line(start_x, start_y, x, y, fill='blue', width=5)
        tag=random.randint(0,100000)
        canvas.itemconfig(line,tags=f"line-{tag}")
        canvas.tag_bind(f"line-{tag}","<Button-1>",lambda event:handleLineClick(event, line))
        endDrawingLine()
    elif is_drawing_rectangle:
        rectangle=canvas.create_rectangle((start_x, start_y, x, y), fill = 'purple',width=3)
        tag=random.randint(0,100000)
        canvas.itemconfig(rectangle,tags=f"rectangle-{tag}")
        canvas.tag_bind(f"rectangle-{tag}","<Button-1>",lambda event:handleRectangleClick(event, rectangle))
        endDravingRectangle()
    elif is_drawing_circle:
        radius = math.dist([start_x,start_y], [x,y])
        center_x, center_y = midpoint(start_x, start_y, x, y)
        circle=canvas.create_oval([center_x-radius,center_y-radius,center_x+radius,center_y+radius],fill = 'green',width=3)
        tag=random.randint(0,100000)
        canvas.itemconfig(circle,tags=f"circle-{tag}")
        canvas.tag_bind(f"circle-{tag}","<Button-1>",lambda event:handleCircleClick(event, circle))
        endDravingCircle()
    else:
        selected_shape = None

window=tk.Tk()
window.title("Zadanie 1 Magda Zaborowska")
window.geometry('1000x750')

label = ttk.Label(window,text='Shapes :D')
label.grid(row=0,columnspan=6)

window.columnconfigure(0)
window.columnconfigure(6, weight=2)


##################################################
###################### LINE ######################
##################################################

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
var_line_button.set('Add line')
line_button = ttk.Button(command=addLine,textvariable=var_line_button)
line_button.grid(row=2, column=5,sticky='ew')

##################################################
#################### Rectangle ###################
##################################################

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
var_rectangle_button.set('Add rectangle')
rectangle_button = ttk.Button(textvariable=var_rectangle_button, command=addRectangle)
rectangle_button.grid(row=4, column=5,sticky='ew')


##################################################
#################### # Circle ####################
##################################################

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
var_circle_button.set('Add circle')
circle_button = ttk.Button(textvariable=var_circle_button,command=addCircle)
circle_button.grid(row=6, column=4,sticky='ew')

canvas=tk.Canvas(window, bg='white',height=500, width=900,relief=tk.RIDGE, bd=0)
canvas.grid(row=7,column=0,columnspan=7)

canvas.bind("<Button-1>", on_canvas_click)
canvas.bind("<B1-Motion>", on_canvas_drag)   # Przeciąganie
canvas.bind("<ButtonRelease-1>", on_canvas_release)

##################################################
################## Bottom buttons ################
##################################################

var_draw_line_button=tk.StringVar()
var_draw_line_button.set('Draw line')
draw_line_button = ttk.Button(textvariable=var_draw_line_button, command=startDrawingLine)
draw_line_button.grid(row=8, column=1, columnspan=2, sticky='ew')

var_draw_rectangle_button=tk.StringVar()
var_draw_rectangle_button.set('Draw rectangle')
draw_rectangle_button = ttk.Button(textvariable=var_draw_rectangle_button, command=startDrawingRectangle)
draw_rectangle_button.grid(row=8, column=3, columnspan=2, sticky='ew')

var_draw_circle_button=tk.StringVar()
var_draw_circle_button.set('Draw circle')
draw_circle_button = ttk.Button(textvariable=var_draw_circle_button, command=startDrawingCircle,width=50)
draw_circle_button.grid(row=8, column=5,columnspan=2,  sticky='w')

var_can_draw=tk.IntVar()
can_draw=ttk.Checkbutton(window,text='Change position mode',variable=var_can_draw, onvalue=1, offvalue=0)
can_draw.grid(row=9, column=1,columnspan=2)

var_save_button = tk.StringVar()
var_save_button.set('Save')
save_button = ttk.Button(textvariable=var_save_button, command=save_coordinates)
save_button.grid(row=9, column=3, sticky='ew')

var_read_button = tk.StringVar()
var_read_button.set('Read File')
read_button = ttk.Button(textvariable=var_read_button, command=read_coordinates)
read_button.grid(row=9, column=4, sticky='ew')

reset_button = ttk.Button(text="Reset", command=reset,width=24)
reset_button.grid(row=9, column=5, sticky='ew')

var_change_shape_button = tk.StringVar()
var_change_shape_button.set('Change Shape')
change_shape_button = ttk.Button(textvariable=var_change_shape_button, command=enable_shape_change,width=24)
change_shape_button.grid(row=9, column=6, sticky='w')

window.mainloop()