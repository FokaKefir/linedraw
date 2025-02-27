from random import *
import os
import json
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


def lines_to_image(lines, resolution, h, w):
    line_width = 4
    img = Image.new("RGB",(resolution,resolution*h//w),(255,255,255))
    draw = ImageDraw.Draw(img)
    if (type(lines) == dict):
        for color in lines:
            for l in lines[color]:
                if color == 'black':
                    draw.line(l, (0, 0, 0), line_width)
                elif color == 'red':
                    draw.line(l, (255, 0, 0), line_width)
                elif color == 'green':
                    draw.line(l, (0, 255, 0), line_width)
                elif color == 'blue':
                    draw.line(l, (0, 0, 255), line_width)
                elif color == 'cyan':
                    draw.line(l, (0, 255, 255), line_width)
                elif color == 'magenta':
                    draw.line(l, (255, 0, 255), line_width)
                elif color == 'yellow':
                    draw.line(l, (255, 255, 0), line_width)
    else:
        for l in lines:
            draw.line(l,(0,0,0),line_width)

    return img

def save_to_bitmap(lines, resolution, h, w, contour_simplify, hatch_size, path):
    if not os.path.exists('./bitmap/'):
        os.mkdir('bitmap')

    file_name, _ = os.path.splitext(os.path.basename(path))

    img = lines_to_image(lines, resolution, h, w)
    img.save(f'bitmap/{file_name}_cs{contour_simplify}_hs{hatch_size}.jpg')

def display_bitmap(lines, resolution, h, w):
    disp = lines_to_image(lines, resolution, h, w)
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

def save_to_json(lines, contour_simplify, hatch_size, path, h, w):
    if not os.path.exists('./json/'):
        os.mkdir('json')
    
    file_name, _ = os.path.splitext(os.path.basename(path))

    if (type(lines) == list):
        lines = {'black': lines}

    json_data = {
        'width': w,
        'height': h,
        'lines': lines
    }

    with open(f'json/{file_name}_cs{contour_simplify}_hs{hatch_size}.json', 'w') as fout:
        json.dump(json_data, fout) 
