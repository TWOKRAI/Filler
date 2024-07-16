# import qdarktheme

# dark_stylesheet = qdarktheme.load_stylesheet("light")


def style( color):
    if color == 'green':
        with open('filler_interface/Style_windows/style_green.css', 'r') as f:
            custom_style = f.read()
    elif color == 'blue':
        with open('Style_windows/style_blue.css', 'r') as f:
            custom_style = f.read()

    #return dark_stylesheet + custom_style
    return custom_style