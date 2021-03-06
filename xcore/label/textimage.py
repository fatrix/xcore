# encoding: utf-8

from PIL import Image, ImageChops, ImageDraw,\
    ImageFilter, ImageFont, ImageColor
from StringIO import StringIO
from django.conf import settings
import os

# global var
fonts = {}


def setup_font_list():
    """
    setup function for the font_list; searches for fontfiles in the 'font'-directory in the xcore-app
    and in the project-specific directory specified in settings.XCORE_FONTS_DIR
    """
    path_list = getattr(settings, 'XCORE_FONTS_DIR', [])
    path_list.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "font"))

    for path in path_list:
        for root, dirnames, filenames in os.walk(path):
            for file in filenames:
                if file.endswith('.ttf') or file.endswith('.otf'):
                    f_name = file.replace(".ttf", "")
                    f_name = file.replace(".otf", "")
                    font = ImageFont.truetype(os.path.join(root, file), 12)
                    name = "%s %s" % (font.getname()[0], font.getname()[1])

                    f_dict = {'name': name,
                              'file': os.path.join(root, file)
                    }
                    fonts[name] = f_dict


def get_label(text="TEXT", text_color="white", text_size=22, text_font="GeosansLight Regular"):
    """
    Creates the label
    """

    font_config = fonts.get(text_font)
    if not font_config:
        raise Exception("Font %s not found" % text_font)

    font = ImageFont.truetype(font_config['file'], text_size)

    if not font:
        raise Exception("No font found for %s" % text_font)
    output = StringIO()

    # based on http://nedbatchelder.com/blog/200801/truly_transparent_text_with_pil.html

    im = Image.new("RGB", (500, 100), (0, 0, 0))
    alpha = Image.new("L", im.size, "black")

    imtext = Image.new("L", im.size, 0)
    drtext = ImageDraw.Draw(imtext)

    # darken() included for fix lighter color
    drtext.text((1, 1), text, font=font, fill=tohex(darken((inverted(text_color)))))
    w, h = drtext.textsize(text, font=font)

    # get the ligther out of image
    alpha = ImageChops.lighter(alpha, imtext)

    # solidcolor part
    solidcolor = Image.new("RGBA", im.size, text_color)

    # to receive nice borders
    immask = Image.eval(imtext, lambda p: 255 * (int(p != 0)))
    im = Image.composite(solidcolor, im, immask)
    im.putalpha(alpha)
    im.filter(ImageFilter.SMOOTH_MORE)

    shadowc = im.crop((0, 0, w + 3, h + 3))
    shadowc.load()

    blur_f = 10
    count = 0

    while count < blur_f:
        shadowc.filter(ImageFilter.BLUR)
        count += 1

    shadowc.save(output, "PNG", quality=50)
    return output, {'width': w + 3, 'height': h + 3}


def inverted(color):
    """
    invert RGB-color
    """
    rgb = ImageColor.getrgb(color)
    inv = 255
    return inv - rgb[0], inv - rgb[1], inv - rgb[2]


def tohex(rgb):
    """
    from http://blog.affien.com/archives/2004/12/20/rgb-to-hex-and-why-the-python-interactive-mode-is-so-damned-handy/
    converts a RGB-color to hexadecimal format
    """
    return "#%02X%02X%02X" % (rgb[0], rgb[1], rgb[2])


def darken(rgb, darken_factor=0.2, rgb_darker=[]):
    """
    makes a RGB-color darker
    """
    for v in rgb:
        v = v / darken_factor
        if (v > 255):
            v = 255
        rgb_darker.append(v)
    return rgb_darker

setup_font_list = setup_font_list()
