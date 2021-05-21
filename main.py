#OpenCV for image processing
import cv2
#easygui to allow selection of file from our system
import easygui
#numpy to store images , processed as numbers
import numpy as np
#imageio to read the file choosen by filebox using path
import imageio
import sys
#matplot lib for vizualization and plotting
import matplotlib.pyplot as plt
#os for os interaction, to read and save images of path
import os
#for enabling GUI aplications
import tkinter as tk
from tkinter import filedialog
from tkinter import *
#python imaging library for saving different image file formats
from PIL import ImageTk, Image

#Making the main window
top=tk.Tk()
top.geometry('400x400')
top.title('Cartoonify Your Image !')
top.configure(background='white')
label=Label(top,background='#CDCDCD', font=('calibri',20,'bold'))

#Building a filebox to choose a particular file
def upload():
    ImagePath=easygui.fileopenbox()
    cartoonify(ImagePath)

#Elaborating the function cartoonify
def cartoonify(ImagePath):
    #To store the image in form of nos. use the Imread method
    # reading the image
    originalmage = cv2.imread(ImagePath)
    originalmage = cv2.cvtColor(originalmage, cv2.COLOR_BGR2RGB)
    #print(image)  # image is stored in form of numbers

    # confirm that image is chosen
    if originalmage is None:
        print("Can not find any image. Choose appropriate file")
        sys.exit()
    # to display all images at a similar scale at last we resize them
    ReSized1 = cv2.resize(originalmage, (960, 540))
    #plt.imshow(ReSized1, cmap='gray') for checking purpose


    #converting an image to grayscale
    # using the cvtColor(image, flag) method to transform color, here BGR2GRAY returns in grayscale.
    grayScaleImage= cv2.cvtColor(originalmage, cv2.COLOR_BGR2GRAY)
    ReSized2 = cv2.resize(grayScaleImage, (960, 540))
    #plt.imshow(ReSized2, cmap='gray') for getting more clear insights into every single transformation

    #Smoothening a grayscale image 
    #applying median blur to smoothen an image
    smoothGrayScale = cv2.medianBlur(grayScaleImage, 5)
    ReSized3 = cv2.resize(smoothGrayScale, (960, 540))
    #plt.imshow(ReSized3, cmap='gray') for confirmation

    #retrieving the edges and highlighting them for cartoon effect
    #threshold value is the mean of the neighborhood pixel values area minus the constant C. C is a constant that is subtracted from the mean or weighted sum of the neighborhood pixels
    #so now by using thresholding technique
    getEdge = cv2.adaptiveThreshold(smoothGrayScale, 255, 
        cv2.ADAPTIVE_THRESH_MEAN_C, 
        cv2.THRESH_BINARY, 9, 9)

    ReSized4 = cv2.resize(getEdge, (960, 540))
    #plt.imshow(ReSized4, cmap='gray')

    #Preparing a mask image / light color image
    #applying bilateral filter to remove noise 
    #and keep edge sharp as required for cartoonifying (,,diameter of pixel,signmacolor , sigma space) 
    #make image look more vicious and like water paint
    colorImage = cv2.bilateralFilter(originalmage, 9, 300, 300)
    ReSized5 = cv2.resize(colorImage, (960, 540))
    #plt.imshow(ReSized5, cmap='gray')


    #masking edged image with our "BEAUTIFY" image
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)

    ReSized6 = cv2.resize(cartoonImage, (960, 540))
    #plt.imshow(ReSized6, cmap='gray') to check the bitwise masking 

    # Plotting the whole transition together 
    images=[ReSized1, ReSized2, ReSized3, ReSized4, ReSized5, ReSized6]
    #list containing all images 
    fig, axes = plt.subplots(3,2, figsize=(8,8), subplot_kw={'xticks':[], 'yticks':[]}, gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')
    #to display one one images in each block

    #Making a save button in the main window
    save1=Button(top,text="Save cartoon image",command=lambda: save(ReSized6, ImagePath),padx=30,pady=5)
    save1.configure(background='#364156', foreground='white',font=('calibri',10,'bold'))
    save1.pack(side=TOP,pady=50)
    
    plt.show()
    
# functionality of the save button
def save(ReSized6, ImagePath):
    #saving an image using imwrite()
    newName="cartoonified_Image"
    path1 = os.path.dirname(ImagePath) #to extract head path of the file path
    extension=os.path.splitext(ImagePath)[1] #to extract extension of the file from path
    path = os.path.join(path1, newName+extension) #forms complete path for saving the new image
    cv2.imwrite(path, cv2.cvtColor(ReSized6, cv2.COLOR_RGB2BGR)) #to save the file at the path mentioned
    I= "Image saved by name " + newName +" at "+ path 
    tk.messagebox.showinfo(title=None, message=I)

#making the cartoonify button in the main window
upload=Button(top,text="Cartoonify an Image",command=upload,padx=10,pady=5)
upload.configure(background='#364156', foreground='white',font=('calibri',10,'bold'))
upload.pack(side=TOP,pady=50)

#main function to build the tkinter window
top.mainloop()

