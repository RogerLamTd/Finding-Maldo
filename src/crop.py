from PIL import Image
import random

def crop_image(img):
    im_w, im_h = img.size

    # max y-axis variation
    max_hfactor_val = im_h - 500

    # max x-axis variation
    max_wfactor_val = im_w - 500

    # get random shift in y-axis, x-axis rounded to nearest integer
    randh = int(max_hfactor_val*random.random())
    randw = int(max_wfactor_val*random.random())

    print("new lower bound on image w: {}, h: {}".format(randh, randw))

    # box = (x0, y0, x1, y1) -> x0 = left boundary y0 = up boundary ...
    x0 = randw
    y0 = randh
    x1 = randw + 500
    y1 = randh + 500
    ret_img = img.crop((x0, y0, x1, y1))
    return [ret_img, x0, y0]