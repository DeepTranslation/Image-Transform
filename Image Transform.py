# coding: utf-8
# Matrix transformations on images


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
#parser.add_argument("-h", "--help", help="Linear transformation of images.")

parser.add_argument("-i", "--inputfile", help="Image file to be transformed")
parser.add_argument("-o", "--outputfile", help="name of the outputfile")
parser.add_argument("-sc", "--scale",  type=float, help="scales the image by the factor", action=CustomAction)
#parser.add_argument("-sh", "--scale", type=float, help="scales the image by the factor")
parser.add_argument("-r", "--rotate", type=float, help="Rotates the image by angle", action=CustomAction)
parser.add_argument("-m", "--mirror", type=float, help="Mirrors along the mirror axis defined by its angle", action=CustomAction)




args = parser.parse_args()

print(args.inputfile)
print(args.outputfile)
print(args.ordered_args)



# Open image file as numpy array


try:
    img = Image.open(args.inputfile, 'r')
except IOError as e:
    print('cannot open', args.inputfile)
    print( "I/O error({0}): {1}".format(e.errno, e.strerror))
    sys.exit(1)
#img = Image.open(FILE)
imageArray = np.asarray(img)
imageWidth=imageArray.shape[1]
imageHeight=imageArray.shape[0]
print(imageArray.shape)




# Plot image array
#plt.figure()
#plt.imshow(imageArray)
#plt.show()

trfMatrix=np.array([[1,0],[0,1]])

def horizontalShear (s):
    # horizontal shear (-2<=s<=2)
    return np.array([[1,0],[s,1]])

def verticalShear (s):
    # vertical shear (-2<=s<=2)
    return np.array([[1,s],[0,1]])

def horizontalScaling (h):
    # horizontal scaling
    # absolute values > 1 =  decreasing size
    # absolute values between 0 and 1 =  increasing size
    # values below 0 = mirroring
    return np.array([[1,0],[0,h]])

def verticalScaling (v):
    #  vertical scaling
    # absolute values > 1 =  decreasing size
    # absolute values between 0 and 1 =  increasing size
    # values below 0 = mirroring
    return np.array([[v,0],[0,1]])

def rotation (angle):
    #  rotation
    # angle in degrees
    angle=math.radians(angle)
    return np.array([[math.cos(alpha),math.sin(alpha)],[-math.sin(alpha),math.cos(alpha)]])


def mirroring (angle):
    #  mirroring
    # angle in degrees
    angle=math.radians(angle)
    return np.array([[math.cos(alpha),math.sin(alpha)],[math.sin(alpha),-math.cos(alpha)]])


print(args.ordered_args[0][1])
trfMatrix=trfMatrix.dot(shear(args.ordered_args[0][1]))
#trfMatrix*=shear(args.ordered_args[0][1])

'''

# show new coordinates, if so desired
# newcoordinateArray




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

'''
# mirroring
#alpha = math.pi/3
#trfMatrix=np.array([[math.cos(alpha),math.sin(alpha)],[math.sin(alpha),-math.cos(alpha)]])


# make array with new coordinates by multiplying 
# transformation matrix with the coordinates
# null point in the middle of the image
newcoordinateArray=np.asarray([[trfMatrix.dot([y,x])] 
                               for y in range(-round(imageHeight/2),round(imageHeight/2))
                               for x in range(-round(imageWidth/2),round(imageWidth/2))]).reshape(imageHeight,imageWidth,2)
newcoordinateArray.shape


# Transform image by storing the pixel values for each pixel in the new image
# from the calculated coordinates in original images

transformedImage=np.asarray([imageArray[int(round(newcoordinateArray[y,x,0]+imageHeight/2)),
                            int(round(newcoordinateArray[y,x,1]+imageWidth/2))] if 
                  int(round(newcoordinateArray[y,x,0]+imageHeight/2)) in range(0,imageHeight-1) and
                      int(round(newcoordinateArray[y,x,1]+imageWidth/2)) in range (0,imageWidth-1)
                             else imageArray[0,0]  for y in range(imageHeight)for x in range(imageWidth)])



# show shapes of the transformed image array, if so desired
# transformedImage.shape
# transformedImage.reshape(imageHeight,imageWidth,3).shape


# Plot image array
plt.figure()
plt.imshow(transformedImage.reshape(imageHeight,imageWidth,3))
plt.show()


# Save Image
img= Image.fromarray(transformedImage.reshape(imageHeight,imageWidth,3))
img.save(args.outputfile)
sys.exit(1)

'''

def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print 'test.py -i <inputfile> -o <outputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'test.py -i <inputfile> -o <outputfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   print 'Input file is "', inputfile
   print 'Output file is "', outputfile

if __name__ == "__main__":
   main(sys.argv[1:])

   '''