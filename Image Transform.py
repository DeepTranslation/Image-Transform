
# coding: utf-8

# Matrix transformations on images

# In[14]:


import math, sympy, numpy

import matplotlib.image as mpimg

import numpy as np
import matplotlib.pyplot as plt
import PIL
from PIL import Image


# In[8]:


# set display Options for jupyter notebook
np.set_printoptions(linewidth=180)


# In[17]:


# Open image file as numpy array
file = "BellenA2.jpg"
img = Image.open(file)
imageArray = np.asarray(img)
imageWidth=imageArray.shape[1]
imageHeight=imageArray.shape[0]
print(imageArray.shape)


# In[16]:


# Plot image array
plt.figure()
plt.imshow(imageArray)
plt.show()


# In[204]:


# show new coordinates, if so desired
# newcoordinateArray


# In[267]:


#create transformation matrix
# horizontal shear (-2<=s<=2)
s=-2
trfMatrix=np.array([[1,0],[s,1]])
# vertical shear (-2<=s<=2)
s=-2
trfMatrix=np.array([[1,s],[0,1]])

# horizontal and vertical scaling
# absolute values > 1 =  decreasing size
# absolute values between 0 and 1 =  increasing size
# values below 0 = mirroring


v = -2 # vertical scalar
h = 1 # horizontal scalar
trfMatrix=np.array([[v,0],[0,h]])

# rotation
alpha=math.pi/5
trfMatrix=np.array([[math.cos(alpha),math.sin(alpha)],[-math.sin(alpha),math.cos(alpha)]])

# mirroring
alpha = math.pi/3
trfMatrix=np.array([[math.cos(alpha),math.sin(alpha)],[math.sin(alpha),-math.cos(alpha)]])


# In[268]:


# make array with new coordinates by multiplying 
# transformation matrix with the coordinates
# null point in the middle of the image
newcoordinateArray=np.asarray([[trfMatrix.dot([y,x])] 
                               for y in range(-round(imageHeight/2),round(imageHeight/2))
                               for x in range(-round(imageWidth/2),round(imageWidth/2))]).reshape(imageHeight,imageWidth,2)
newcoordinateArray.shape


# In[269]:


# Transform image by storing the pixel values for each pixel in the new image
# from the calculated coordinates in original images

transformedImage=np.asarray([imageArray[int(round(newcoordinateArray[y,x,0]+imageHeight/2)),
                            int(round(newcoordinateArray[y,x,1]+imageWidth/2))] if 
                  int(round(newcoordinateArray[y,x,0]+imageHeight/2)) in range(0,imageHeight-1) and
                      int(round(newcoordinateArray[y,x,1]+imageWidth/2)) in range (0,imageWidth-1)
                             else imageArray[0,0]  for y in range(imageHeight)for x in range(imageWidth)])


# In[205]:


# show shapes of the transformed image array, if so desired
# transformedImage.shape
# transformedImage.reshape(imageHeight,imageWidth,3).shape


# In[270]:


# Plot image array
plt.figure()
plt.imshow(transformedImage.reshape(imageHeight,imageWidth,3))
plt.show()


# In[271]:


# Save Image
img= Image.fromarray(transformedImage.reshape(imageHeight,imageWidth,3))
img.save("Transform1.png")

