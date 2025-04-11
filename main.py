import linedraw


if  __name__ == '__main__':
    img_name = 'tesla_color'
    img_format = '.png'

    draw_contours = True
    contour_simplify = 3

    draw_hatch = True
    hatch_size = 24

    linedraw.contour_simplify = contour_simplify
    linedraw.hatch_size = hatch_size
    linedraw.draw_contours = draw_contours
    linedraw.draw_hatch = draw_hatch
    linedraw.color_type = 'cmyk'
    linedraw.save_bitmap = True
    linedraw.no_svg = False
    linedraw.save_json = True
    #linedraw.export_path = f"output/{img_name}_cs{contour_simplify}_hs{hatch_size}_cmyk.svg"
    linedraw.sketch(f'images/{img_name}{img_format}')
