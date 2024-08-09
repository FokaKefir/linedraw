import linedraw


if  __name__ == '__main__':
    img_name = 'dl1'
    img_format = '.jpeg'

    contour_simplify = 3
    hatch_size = 8

    linedraw.contour_simplify = contour_simplify
    linedraw.hatch_size = hatch_size
    linedraw.color_type = 'cmyk'
    linedraw.save_bitmap = True
    linedraw.no_svg = True
    linedraw.export_path = f"output/{img_name}_cs{contour_simplify}_hs{hatch_size}_cmyk.svg"
    linedraw.sketch(f'images/{img_name}{img_format}')
