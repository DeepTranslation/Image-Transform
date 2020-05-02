# coding: utf-8
# Matrix transformations on images
# Applies various matrix transformations on an image 


import sys
import argparse
import math
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

class CustomAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if not 'ordered_args' in namespace:
            setattr(namespace, 'ordered_args', [])
        previous = namespace.ordered_args
        previous.append((self.dest, values))
        setattr(namespace, 'ordered_args', previous)
parser = argparse.ArgumentParser()
parser.add_argument("inputfile", help="Image file to be transformed")
parser.add_argument("outputfile", help="name of the outputfile")
parser.add_argument("-sc", "--scale",  type=float, help="scales the image horizontally and vertically by the factor", action=CustomAction)
parser.add_argument("-sch", "--scaleHorizontally",  type=float, help="scales the image horizontally by the factor", action=CustomAction)
parser.add_argument("-scv", "--scaleVertically",  type=float, help="scales the image vertically by the factor", action=CustomAction)
parser.add_argument("-sh", "--shear",  type=float, help="shears the image horizontally and vertically by the factor", action=CustomAction)
parser.add_argument("-shh", "--shearHorizontally",  type=float, help="shears the image horizontally by the factor", action=CustomAction)
parser.add_argument("-shv", "--shearVertically",  type=float, help="shears the image vertically by the factor", action=CustomAction)
parser.add_argument("-r", "--rotate", type=float, help="Rotates the image by angle", action=CustomAction)
parser.add_argument("-m", "--mirror", type=float, help="Mirrors along the mirror axis defined by its angle", action=CustomAction)

args = parser.parse_args()

def scale (f):
    # horizontal and vertical scaling
    # absolute factor values > 1 =  increasing size
    # absolute values between 0 and 1 = decreasing  size
    # values below 0 = mirroring
    return np.array([[1/f,0],[0,1/f]])

def scaleHorizontally (h):
    # horizontal scaling
    # absolute values > 1 =  decreasing size
    # absolute values between 0 and 1 =  increasing size
    # values below 0 = mirroring
    return np.array([[1,0],[0,1/h]])

def scaleVertically (v):
    #  vertical scaling
    # absolute values > 1 =  decreasing size
    # absolute values between 0 and 1 =  increasing size
    # values below 0 = mirroring
    return np.array([[1/v,0],[0,1]])

def shear (s):
    # horizontal and vertical shear 
    # useful values: (-2<=s<=2)
    return np.array([[1,s],[s,1]])

def shearHorizontally (s):
    # horizontal shear 
    # useful values: (-2<=s<=2)
    return np.array([[1,0],[s,1]])

def shearVertically (s):
    # vertical shear (-2<=s<=2)
    return np.array([[1,s],[0,1]])

def rotate (angle):
    #  rotation
    # angle in degrees
    angle=math.radians(angle)
    return np.array([[math.cos(angle),math.sin(angle)],[-math.sin(angle),math.cos(angle)]])

def mirror (angle):
    #  mirroring
    # angle in degrees
    angle=math.radians(angle)
    return np.array([[math.cos(angle),math.sin(angle)],[math.sin(angle),-math.cos(angle)]])


print(args.inputfile)
print(args.outputfile)

try:
    img = Image.open(args.inputfile, 'r')
except IOError as e:
    print('cannot open', args.inputfile)
    print( "I/O error({0}): {1}".format(e.errno, e.strerror))
    sys.exit(1)

imageArray = np.asarray(img)
imageWidth=imageArray.shape[1]
imageHeight=imageArray.shape[0]
print(imageArray.shape)

# Plot image array
#plt.figure()
#plt.imshow(imageArray)
#plt.show()

# Define identity transformation matrix as a starting point 
# in case no transformation is specified
trfMatrix=np.array([[1,0],[0,1]])


# multiply the transformation matrix with the optional command line arguments

# eval(args.ordered_args[0][0]) is the function to be called
# args.ordered_args[0][1] is the value to use for the function
try:
    print(args.ordered_args)
    for i in range(len(args.ordered_args)):
        trfMatrix=trfMatrix.dot(eval(args.ordered_args[i][0])(args.ordered_args[i][1]))
except AttributeError:
    print("no transformation specified")


# make array with new coordinates by multiplying 
# transformation matrix with the coordinates
# null point in the middle of the image
newcoordinateArray=np.asarray([[trfMatrix.dot([y,x])] 
                               for y in range(-round(imageHeight/2),round(imageHeight/2))
                               for x in range(-round(imageWidth/2),round(imageWidth/2))]).reshape(imageHeight,imageWidth,2)


# Transform image by storing the pixel values for each pixel in the new image
# from the calculated coordinates in original images

transformedImage=np.asarray([imageArray[int(round(newcoordinateArray[y,x,0]+imageHeight/2)),
                            int(round(newcoordinateArray[y,x,1]+imageWidth/2))] if 
                  int(round(newcoordinateArray[y,x,0]+imageHeight/2)) in range(0,imageHeight-1) and
                      int(round(newcoordinateArray[y,x,1]+imageWidth/2)) in range (0,imageWidth-1)
                             else imageArray[0,0]  for y in range(imageHeight)for x in range(imageWidth)])


# Plot image array
plt.figure()
plt.imshow(transformedImage.reshape(imageHeight,imageWidth,3))
plt.show()

# Save Image
img= Image.fromarray(transformedImage.reshape(imageHeight,imageWidth,3))
img.save(args.outputfile)
sys.exit(1)
