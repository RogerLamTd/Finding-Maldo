from PIL import Image
import random
from google.cloud import vision
from matplotlib import pyplot as plt 
from matplotlib import patches as pch 

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

def pick_face(content):
    
    face_coords = []
    
    image = vision.Image(content=content)

    response = client.face_detection(image=image, max_results=50)
    faces = response.face_annotations
    
    a = plt.imread(path)
    fig, ax = plt.subplots(1)
    ax.imshow(a)
    

    for face in faces:
        vertices = ([(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])
        
        face_coords.append(vertices)
        
        #print('face bounds: ', vertices)
        # vertices are as follows: top left, top right, bottom right, bottom left.
    
        #rect = pch.Rectangle(vertices[0], (vertices[1][0] -  vertices[0][0]), 
        #                (vertices[2][1] - vertices[0][1]), linewidth = 1, edgecolor ='r', facecolor ='none') 
        # pch.Rectangle( (26, 453), 20, 23)
        
        #ax.add_patch(rect)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    
    randint = int((len(faces)*random.random())
    chosen_face = face_coords[randint]
    rect = pch.Rectangle(chosen_face[0], (vertices[1][0] -  vertices[0][0]), 
                        (vertices[2][1] - vertices[0][1]), linewidth = 1, edgecolor ='r', facecolor ='none')
    ax.add_patch(rect)
        
    return chosen_face
# return type is a list of lists of tuples representing where each internal list represents a face, and each
# tuple is a coordinate of the face; top left, top right, bottom right, bottom left respectively.

def makeMask(face):


def get_Mask(base):
    tagImage, cropX, cropY = crop_image(base)
    faceBox = pick_face(tagImage)
    maskImg = makeMask(face)
    return (maskImg, cropX + faceBox[0][0], cropY + faceBox[0][1])