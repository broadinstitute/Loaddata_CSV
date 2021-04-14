from PIL import Image
from pathlib import Path
from tqdm import tqdm
import glob
import os
import pandas as pd
from re import search
import matplotlib.pyplot as plt
import skimage.io as io
import string
import numpy as np
import re


path = '/home/ubuntu/bucket/projects'
projdir = '2015_10_05_DrugRepurposing_AravindSubramanian_GolubLab_Broad'
batchname = '2016_04_01_a549_48hr_batch1'
platename = 'SQ00015096__2016-06-08T17_05_23-Measurement1'




imgpath = path + "/" + projdir + "/" + batchname + "/" + 'images' + '/' + platename + '/' + "Images"


path=[]
img_names = []

for i, image in enumerate(os.listdir(imgpath)):
    
    imagpath = imgpath + "/" + image
    if imagpath.endswith("tiff"):
        
        head, tail = os.path.split(imagpath)
        img_names.append(tail)
        
        path.append(imagpath)

## extracting metadata from image file name and defining into groups
pattern = re.compile("r(?P<row>\d+)c(?P<column>\d+)f(?P<field>\d+)p(?P<site>\d+)-ch(?P<channelnumber>\d+)")


## apply this regrex to all the imagelist

match = [pattern.match(i) for i in img_names]
row = [r.group("row") for r in match]
col= [c.group("column") for c in match]
field= [f.group("field") for f in match]
site= [s.group("site") for s in match]
channel= [ch.group("channelnumber") for ch in match]

## Defining Well names

rc = [r+c for r, c in zip(row, col)]

well_assignment= {'01' : "A",'02': "B",'03':"C",'04':"D",
                  '05': "E",'06':"F",'07':"G",'08':"H",
                  '09':"I",'10':"J",'11':"K",'12':"L",
                  '13':"M",'14':"N",'15':"O",'16':"P"
}

well = [well_assignment.get(i[0:2])+i[2:] for i in rc]



