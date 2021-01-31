from PIL import Image
import random
import os
from io import BytesIO
from google.cloud import vision
#from matplotlib import pyplot as plt 
#from matplotlib import patches as pch 


os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

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

def pick_face(crop):
    
    face_coords = []
    
    img_byte_arr = BytesIO()
    crop.save(img_byte_arr, format='JPEG')
    image = vision.Image(content=img_byte_arr.getvalue())

    client = vision.ImageAnnotatorClient()

    response = client.face_detection(image=image, max_results=50)
    faces = response.face_annotations
    
    #a = plt.imread(img_byte_arr, format = "JPEG")
    #fig, ax = plt.subplots(1)
    #ax.imshow(a)
    
    for face in faces:
        vertices = ([(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])
        
        face_coords.append((vertices,face.detection_confidence))
        
        print('face bounds: ', vertices)
        #vertices are as follows: top left, top right, bottom right, bottom left.
    
        #rect = pch.Rectangle(vertices[0], (vertices[1][0] -  vertices[0][0]), 
                        #(vertices[2][1] - vertices[0][1]), linewidth = 1, edgecolor ='r', facecolor ='none') 
        #pch.Rectangle( (26, 453), 20, 23)
        
        #ax.add_patch(rect)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    
    filtered_faces = []

    for f in face_coords:
        if f[1] >= 0.65:
            filtered_faces.append(f[0])
            
            
           #rect = pch.Rectangle(f[0][0], (f[0][1][0] - f[0][0][0]), (f[0][2][1] - f[0][0][1])
            #                        , linewidth = 1, edgecolor ='r', facecolor ='none')
            #ax.add_patch(rect)

    randint = random.randint(0, len(filtered_faces) -1)
    
    chosen_face = filtered_faces[randint]
    #rect = pch.Rectangle(chosen_face[0], (chosen_face[1][0] - chosen_face[0][0]), (chosen_face[2][1] - chosen_face[0][1])
                                    #, linewidth = 1, edgecolor ='r', facecolor ='none')
    #ax.add_patch(rect)
    
    #rect = pch.Rectangle(chosen_face[0], (vertices[1][0] -  vertices[0][0]), 
    #                    (vertices[2][1] - vertices[0][1]), linewidth = 1, edgecolor ='r', facecolor ='none')
    #ax.add_patch(rect)
    #fig.savefig("plot.png")
        
    return chosen_face
# return type is a list of lists of tuples representing where each internal list represents a face, and each
# tuple is a coordinate of the face; top left, top right, bottom right, bottom left respectively.

def make_Mask(face):
    mask = Image.open("static/bernie_head.png")
    print(face[1][0] - face[0][0], face[3][1] - face[0][1])
    mask = mask.resize((int((face[1][0] - face[0][0]) * 1.2),
                        int((face[3][1] - face[0][1]) * 1.2)))
    return (mask, (mask.width, mask.height))

def get_Mask(base):
    tagImage, cropX, cropY = crop_image(base)
    faceBox = pick_face(tagImage)
    maskImg, maskSize = make_Mask(faceBox)
    return (maskImg, cropX + faceBox[0][0], cropY + faceBox[0][1], maskSize)


#def get_Bernie(base):
    #tagImage, cropX, cropY = crop_image(base)
    #faceBox = pick_face(tagImage)
    #maskImg, maskSize = make_Mask(faceBox)
#
#
    #mask = Image.open("static/bernie_head.png")
    #print(face[1][0] - face[0][0], face[3][1] - face[0][1])
    #mask = mask.resize((face[1][0] - face[0][0], (face[3][1] - face[0][1])// 2))
    #return (mask, (mask.width, mask.height))
#
#    
    #return (maskImg, cropX + faceBox[0][0] + maskSize[0]//2, cropY + faceBox[0][1], maskSize)