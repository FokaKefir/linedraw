import linedraw


if  __name__ == '__main__':
    img_name = 'sapi1'
    img_format = '.jpeg'

    contour_simplify = 0
    hatch_size = 32
    color_type = 'black'

    linedraw.contour_simplify = contour_simplify
    linedraw.hatch_size = hatch_size
    linedraw.color_type = color_type
    linedraw.draw_hatch = True
    linedraw.draw_contours = False

    linedraw.save_bitmap = True
    linedraw.no_svg = True

    linedraw.sketch(f'images/{img_name}{img_format}')
