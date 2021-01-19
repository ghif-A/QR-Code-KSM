#!/usr/bin/env python3

from __future__ import print_function
from pdf2image import convert_from_path
import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2


#Detect and Decode QR Code
def decode(im) : 
  # Find QR codes
  decodedObjects = pyzbar.decode(im)

  # Print results
  for obj in decodedObjects:
    data = obj.data.decode('utf-8')
    print('DecodedData : ', data,'\n')
    
  return decodedObjects

# Display QR code location
def display(im, decodedObjects):

  # Loop over all decoded objects
  for decodedObject in decodedObjects: 
    points = decodedObject.polygon

    # If the points do not form a quad, find convex hull
    if len(points) > 4 : 
      hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
      hull = list(map(tuple, np.squeeze(hull)))
    else : 
      hull = points;
    
    # Number of points in the convex hull
    n = len(hull)

    # Draw the convext hull
    for j in range(0,n):
      cv2.line(im, hull[j], hull[ (j+1) % n], (255,0,0), 3)

  # Display results 
  cv2.imshow("Results", im);
  cv2.waitKey(0);
  
# Main 
if __name__ == '__main__':
  
  #Convert pdf to jpg
  pages = convert_from_path('KSM 13619003 Semester 2 Tahun 20202021.pdf',100)

  #Save the jpg
  for page in pages:
    page.save('KSM.jpg','JPEG')

  # Read image
  im = cv2.imread('KSM.jpg')

  decodedObjects = decode(im)
  display(im, decodedObjects)
