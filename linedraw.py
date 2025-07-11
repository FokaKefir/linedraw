from random import *
import math
import argparse

from PIL import Image, ImageDraw, ImageOps

from tools.filters import *
from tools.strokesort import *
import tools.perlin as perlin
from tools.util import *
from tools.visualize import *
from tools.colorchannels import image_to_cmyk_parts

no_cv = False
no_svg = False
save_json = False
save_bitmap = False
export_path = "output/out.svg"
draw_contours = True
draw_hatch = True
show_bitmap = False
resolution = 1024
hatch_size = 16
contour_simplify = 2
contrast = 10

color_type = "black"

try:
    import numpy as np
    import cv2
except:
    print("Cannot import numpy/openCV. Switching to NO_CV mode.")
    no_cv = True

def find_edges(IM):
    print("finding edges...")
    if no_cv:
        #appmask(IM,[F_Blur])
        appmask(IM,[F_SobelX,F_SobelY])
    else:
        im = np.array(IM) 
        im = cv2.GaussianBlur(im,(3,3),0)
        im = cv2.Canny(im,100,200)
        IM = Image.fromarray(im)
    return IM.point(lambda p: p > 128 and 255)  


def getdots(IM):
    print("getting contour points...")
    PX = IM.load()
    dots = []
    w,h = IM.size
    for y in range(h-1):
        row = []
        for x in range(1,w):
            if PX[x,y] == 255:
                if len(row) > 0:
                    if x-row[-1][0] == row[-1][-1]+1:
                        row[-1] = (row[-1][0],row[-1][-1]+1)
                    else:
                        row.append((x,0))
                else:
                    row.append((x,0))
        dots.append(row)
    return dots
    
def connectdots(dots):
    print("connecting contour points...")
    contours = []
    for y in range(len(dots)):
        for x,v in dots[y]:
            if v > -1:
                if y == 0:
                    contours.append([(x,y)])
                else:
                    closest = -1
                    cdist = 100
                    for x0,v0 in dots[y-1]:
                        if abs(x0-x) < cdist:
                            cdist = abs(x0-x)
                            closest = x0

                    if cdist > 3:
                        contours.append([(x,y)])
                    else:
                        found = 0
                        for i in range(len(contours)):
                            if contours[i][-1] == (closest,y-1):
                                contours[i].append((x,y,))
                                found = 1
                                break
                        if found == 0:
                            contours.append([(x,y)])
        for c in contours:
            if c[-1][1] < y-1 and len(c)<4:
                contours.remove(c)
    return contours


def getcontours(IM,sc=2):
    print("generating contours...")
    IM = find_edges(IM)
    IM1 = IM.copy()
    IM2 = IM.rotate(-90,expand=True).transpose(Image.FLIP_LEFT_RIGHT)
    dots1 = getdots(IM1)
    contours1 = connectdots(dots1)
    dots2 = getdots(IM2)
    contours2 = connectdots(dots2)

    for i in range(len(contours2)):
        contours2[i] = [(c[1],c[0]) for c in contours2[i]]    
    contours = contours1+contours2

    for i in range(len(contours)):
        for j in range(len(contours)):
            if len(contours[i]) > 0 and len(contours[j])>0:
                if distsum(contours[j][0],contours[i][-1]) < 8:
                    contours[i] = contours[i]+contours[j]
                    contours[j] = []

    for i in range(len(contours)):
        contours[i] = [contours[i][j] for j in range(0,len(contours[i]),8)]


    contours = [c for c in contours if len(c) > 1]

    for i in range(0,len(contours)):
        contours[i] = [(v[0]*sc,v[1]*sc) for v in contours[i]]

    for i in range(0,len(contours)):
        for j in range(0,len(contours[i])):
            contours[i][j] = int(contours[i][j][0]+10*perlin.noise(i*0.5,j*0.1,1)),int(contours[i][j][1]+10*perlin.noise(i*0.5,j*0.1,2))

    return contours


def hatch(IM,sc=16):
    print("hatching...")
    PX = IM.load()
    w,h = IM.size
    lg1 = []
    lg2 = []
    for x0 in range(w):
        for y0 in range(h):
            x = x0*sc
            y = y0*sc
            if PX[x0,y0] > 144:
                pass
                
            elif PX[x0,y0] > 64:
                lg1.append([(x,y+sc/4),(x+sc,y+sc/4)])
            elif PX[x0,y0] > 16:
                lg1.append([(x,y+sc/4),(x+sc,y+sc/4)])
                lg2.append([(x+sc,y),(x,y+sc)])

            else:
                lg1.append([(x,y+sc/4),(x+sc,y+sc/4)])
                lg1.append([(x,y+sc/2+sc/4),(x+sc,y+sc/2+sc/4)])
                lg2.append([(x+sc,y),(x,y+sc)])

    lines = [lg1,lg2]
    for k in range(0,len(lines)):
        for i in range(0,len(lines[k])):
            for j in range(0,len(lines[k])):
                if lines[k][i] != [] and lines[k][j] != []:
                    if lines[k][i][-1] == lines[k][j][0]:
                        lines[k][i] = lines[k][i]+lines[k][j][1:]
                        lines[k][j] = []
        lines[k] = [l for l in lines[k] if len(l) > 0]
    lines = lines[0]+lines[1]

    for i in range(0,len(lines)):
        for j in range(0,len(lines[i])):
            x, y = lines[i][j]
            x = int(x + sc * perlin.noise(i * 0.5, j * 0.1, 1))
            y = int(y + sc * perlin.noise(i * 0.5, j * 0.1, 2)) - j
            
            x = max(0, min(w * sc - 1, x))
            y = max(0, min(h * sc - 1, y))
            lines[i][j] = (x, y)

    return lines


def sketch(path):
    IM = None
    possible = [path,"images/"+path,"images/"+path+".jpg","images/"+path+".png","images/"+path+".tif"]
    path_to_img = None
    for p in possible:
        try:
            IM = Image.open(p)
            path_to_img = p
            break
        except FileNotFoundError:
            print("The Input File wasn't found. Check Path")
            exit(0)
            pass
    w,h = IM.size

    # if h > w:
    #     IM = IM.rotate(90, expand=True)
    #     w, h = h, w

    if color_type == 'black':
        IM = IM.convert("L")
        IM = ImageOps.autocontrast(IM, contrast)

        lines = []
        if draw_contours:
            lines += getcontours(IM.resize((resolution//contour_simplify,resolution//contour_simplify*h//w)),contour_simplify)
        if draw_hatch:
            lines += hatch(IM.resize((resolution//hatch_size,resolution//hatch_size*h//w)),hatch_size)

        lines = sortlines(lines)
        
    elif color_type == 'rgb':
        im_l = IM.convert("L")
        im_r, im_g, im_b = IM.split()

        im_l = ImageOps.autocontrast(im_l, contrast)
        im_r = ImageOps.autocontrast(im_r, contrast)
        im_g = ImageOps.autocontrast(im_g, contrast)
        im_b = ImageOps.autocontrast(im_b, contrast)

        lines_dict = {}
        for im, color in [(im_l, "black"), (im_r, "red"), (im_g, "green"), (im_b, "blue")]:
            print(f'color: {color}')

            lines = []
            if draw_contours:
                lines += getcontours(im.resize((resolution//contour_simplify,resolution//contour_simplify*h//w)),contour_simplify)
            if draw_hatch:
                lines += hatch(im.resize((resolution//hatch_size,resolution//hatch_size*h//w)),hatch_size)

            lines = sortlines(lines)

            lines_dict[color] = lines

        lines = lines_dict
    
    elif color_type == 'cmyk':
        im_c, im_m, im_y, im_k = image_to_cmyk_parts(IM)
        im_c, im_m, im_y, im_k = [ImageOps.autocontrast(im, contrast) for im in (im_c, im_m, im_y, im_k)]

        lines_dict = {}
        for im, color in [(im_c, "cyan"), (im_m, "magenta"), (im_y, "yellow")]:
            print(f'color: {color}')

            lines = hatch(im.resize((resolution//hatch_size,resolution//hatch_size*h//w)),hatch_size)
            lines = sortlines(lines)
            lines_dict[color] = lines
        
        print('color: black')
        lines = getcontours(im_k.resize((resolution//contour_simplify,resolution//contour_simplify*h//w)),contour_simplify)
        lines = sortlines(lines)
        lines_dict['black'] = lines

        lines = lines_dict

    if show_bitmap:
        display_bitmap(lines, resolution, h, w)

    if not no_svg:
        save_svg(lines, export_path)

    if save_json:
        save_to_json(lines, contour_simplify, hatch_size, path_to_img, h=resolution, w=resolution*h//w)

    if save_bitmap:
        save_to_bitmap(lines, resolution, h, w, contour_simplify, hatch_size, path)

    if (type(lines) == list): 
        print(len(lines),"strokes.")
    elif (type(lines) == dict):
        sum_lines = 0
        for color in lines:
            print(f'{color}: {len(lines[color])} strokes.')
            sum_lines += len(lines[color])
        print(sum_lines, "strokes.")
    print("done.")
    return lines


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert image to vectorized line drawing for plotters.')
    parser.add_argument('-i','--input',dest='input_path',
        default='lenna',action='store',nargs='?',type=str,
        help='Input path')

    parser.add_argument('-o','--output',dest='output_path',
        default=export_path,action='store',nargs='?',type=str,
        help='Output path.')
    
    parser.add_argument('-c', '--color', dest='color_type',
        default=color_type, action='store', type=str,
        choices=['black', 'rgb'],
        help='Color channels which is used')

    parser.add_argument('-b','--show_bitmap',dest='show_bitmap',
        const = not show_bitmap,default= show_bitmap,action='store_const',
        help="Display bitmap preview.")

    parser.add_argument('-nc','--no_contour',dest='no_contour',
        const = draw_contours,default= not draw_contours,action='store_const',
        help="Don't draw contours.")
       
    parser.add_argument('-nh','--no_hatch',dest='no_hatch',
        const = draw_hatch,default= not draw_hatch,action='store_const',
        help='Disable hatching.')

    parser.add_argument('--no_cv',dest='no_cv',
        const = not no_cv,default= no_cv,action='store_const',
        help="Don't use openCV.")
    
    parser.add_argument('--no_svg', dest='no_svg', 
                        const=not no_svg, default=no_svg, action='store_const',
                        help="Don't export to SVG.")


    parser.add_argument('--hatch_size',dest='hatch_size',
        default=hatch_size,action='store',nargs='?',type=int,
        help='Patch size of hatches. eg. 8, 16, 32')
    parser.add_argument('--contour_simplify',dest='contour_simplify',
        default=contour_simplify,action='store',nargs='?',type=int,
        help='Level of contour simplification. eg. 1, 2, 3')

    args = parser.parse_args()
    
    export_path = args.output_path
    draw_hatch = not args.no_hatch
    draw_contours = not args.no_contour
    hatch_size = args.hatch_size
    contour_simplify = args.contour_simplify
    show_bitmap = args.show_bitmap
    no_cv = args.no_cv
    no_svg = args.no_svg
    color_type = args.color_type
    sketch(args.input_path)
