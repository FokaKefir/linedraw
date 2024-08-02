import linedraw
import os

def create_dir_if_not_exists(path):
    if not os.path.exists(path):
        os.mkdir(path)

if __name__ == "__main__":

    img_name = "vg"
    img_format = ".jpeg"

    create_dir_if_not_exists("./output/")
    create_dir_if_not_exists(f"./output/{img_name}/")
    create_dir_if_not_exists(f"./output/{img_name}/contour/")
    create_dir_if_not_exists(f"./output/{img_name}/hatch/")
    create_dir_if_not_exists(f"./output/{img_name}/both/")

    for contour_simplify in [1, 2, 3, 4, 5]:
        linedraw.contour_simplify = contour_simplify
        linedraw.draw_contours = True
        linedraw.draw_hatch = False
        linedraw.export_path = f"output/{img_name}/contour/{img_name}_cs{contour_simplify}_nh.svg"
        
        print(f"Contour simplify: {contour_simplify}, no hatch.")
        linedraw.sketch(f'images/{img_name}{img_format}')

    
    for hatch_size in [4, 8, 16, 32]:
        linedraw.hatch_size = hatch_size
        linedraw.draw_contours = False
        linedraw.draw_hatch = True
        linedraw.export_path = f"output/{img_name}/hatch/{img_name}_nc_hs{hatch_size}.svg"
        
        print(f"No contour, hatch size: {hatch_size}")
        linedraw.sketch(f'images/{img_name}{img_format}')
    
    for contour_simplify in [1, 2, 3, 4, 5]:
        for hatch_size in [4, 8, 16, 32]:
            linedraw.contour_simplify = contour_simplify
            linedraw.hatch_size = hatch_size

            linedraw.draw_contours = True
            linedraw.draw_hatch = True
            linedraw.export_path = f"output/{img_name}/both/{img_name}_cs{contour_simplify}_hs{hatch_size}.svg"

            print(f"Contour simplify: {contour_simplify}, hatch size: {hatch_size}")
            linedraw.sketch(f'images/{img_name}{img_format}')