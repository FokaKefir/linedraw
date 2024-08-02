from random import *
from PIL import Image, ImageDraw, ImageOps

def turtle_visualize(lines):
    import turtle
    wn = turtle.Screen()
    t = turtle.Turtle()
    t.speed(0)
    t.pencolor('red')
    t.pd()
    for i in range(0,len(lines)):
        for p in lines[i]:
            t.goto(p[0]*640/1024-320,-(p[1]*640/1024-320))
            t.pencolor('black')
        t.pencolor('red')
    turtle.mainloop()


def display_bitmap(lines, resolution, h, w):
    disp = Image.new("RGB",(resolution,resolution*h//w),(255,255,255))
    draw = ImageDraw.Draw(disp)
    if (type(lines) == dict):
        for color in lines:
            for l in lines[color]:
                if color == 'black':
                    draw.line(l, (0, 0, 0), 5)
                elif color == 'red':
                    draw.line(l, (255, 0, 0), 5)
                elif color == 'green':
                    draw.line(l, (0, 255, 0), 5)
                elif color == 'blue':
                    draw.line(l, (0, 0, 255), 5)
                elif color == 'cyan':
                    draw.line(l, (0, 255, 255), 5)
                elif color == 'magenta':
                    draw.line(l, (255, 0, 255), 5)
                elif color == 'yellow':
                    draw.line(l, (255, 255, 0), 5)
    else:
        for l in lines:
            draw.line(l,(0,0,0),5)
    disp.show()

def save_svg(lines, export_path):
    f = open(export_path,'w')
    f.write(makesvg(lines))
    f.close()

def makesvg(lines):
    print("generating svg file...")
    out = '<svg xmlns="http://www.w3.org/2000/svg" version="1.1">'
    if (type(lines) == dict):
        for color in lines:
            for l in lines[color]:
                l = ",".join([str(p[0]*0.5)+","+str(p[1]*0.5) for p in l])
                out += '<polyline points="'+l+f'" stroke="{color}" stroke-width="2" fill="none" />\n'
        
    else:
        for l in lines:
            l = ",".join([str(p[0]*0.5)+","+str(p[1]*0.5) for p in l])
            out += '<polyline points="'+l+'" stroke="black" stroke-width="2" fill="none" />\n'
    
    out += '</svg>'
    return out