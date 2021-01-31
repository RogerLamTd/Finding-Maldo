#!/usr/bin/env python
# coding: utf-8

# In[21]:


import io
import os
from google.cloud import vision
from matplotlib import pyplot as plt 
from matplotlib import patches as pch 

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/roger/Documents/GitHub/Finding-Maldo/key.json"
#insert path variable to API key here.

client = vision.ImageAnnotatorClient()



# In[22]:


from PIL import Image
import random

# path variable to full image

crowd_image = Image.open('/Users/roger/Documents/GitHub/Finding-Maldo/mask_test.png')
im_w, im_h = crowd_image.width, crowd_image.height
print("src crowd photo w: {}, h: {}".format(im_w, im_h))

def crop_image(src_height, src_width):

    # max y-axis variation
    max_hfactor_val = im_h - src_height

    # max x-axis variation
    max_wfactor_val = im_w - src_width

    # get random shift in y-axis, x-axis rounded to nearest integer
    randh = int(max_hfactor_val*random.random())
    randw = int(max_wfactor_val*random.random())

    print("new lower bound on image w: {}, h: {}".format(randh, randw))

    # box = (x0, y0, x1, y1) -> x0 = left boundary y0 = up boundary ...
    x0 = randw
    y0 = randh
    x1 = randw + src_width
    y1 = randh + src_height
    print("cropping dimensions left: {}, right: {}, up: {}, down: {}".format(x0, x1, y0, y1))
    ret_img = crowd_image.crop((x0, y0, x1, y1))
    print("cropped photo w: {}, h: {}".format(ret_img.width, ret_img.height))
    ret_img.save("/Users/roger/Documents/GitHub/Finding-Maldo/test_{}_{}.png".format(src_width, src_height))


# In[46]:


def pick_face(path):
    
    face_coords = []
    confidences = []
    
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    
    image = vision.Image(content=content)

    response = client.face_detection(image=image, max_results=100)
    faces = response.face_annotations
    
    a = plt.imread(path)
    fig, ax = plt.subplots(1)
    ax.imshow(a)
    

    for face in faces:


        vertices = ([(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])
        
        face_coords.append((vertices,face.detection_confidence))
        
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
    
    #randint = int(50*random.random())
    #chosen_face = face_coords[randint]
    #rect = pch.Rectangle(chosen_face[0], (vertices[1][0] -  vertices[0][0]), 
                        #(vertices[2][1] - vertices[0][1]), linewidth = 1, edgecolor ='r', facecolor ='none')
    #ax.add_patch(rect)
    
    filtered_faces = []
    for f in face_coords:
        if f[1] >= 0.70:
            filtered_faces.append(f[0])
            
            rect = pch.Rectangle(f[0][0], (f[0][1][0] - f[0][0][0]), (f[0][2][1] - f[0][0][1])
                                 , linewidth = 1, edgecolor ='r', facecolor ='none')
            ax.add_patch(rect)
            
            
    randint = int(len(filtered_faces)*random.random())
    chosen_face = filtered_faces[randint]    
            
    return chosen_face

    #return faces#chosen_face
# return type is a list of lists of tuples representing where each internal list represents a face, and each
# tuple is a coordinate of the face; top left, top right, bottom right, bottom left respectively.


# In[38]:


crop_image(500,500)


# In[45]:


p = pick_face('/Users/roger/Documents/GitHub/Finding-Maldo/test_500_500.png')


# In[35]:


p[0]


# In[ ]:




