import os
import pandas as pd
import numpy as np
import re

path = '/home/ubuntu/bucket/projects'
projdir = '2019_07_11_JUMP-CP'
batchname = '2020_12_08_CPJUMP1_Bleaching'




batchpath = os.path.join(path, projdir, batchname)

fpath = [os.path.join(batchpath, 'images', f) for f in os.listdir(os.path.join(batchpath, 'images'))]

fimages = [os.path.join(i, "Images") for i in fpath]

# outpath = [os.path.join(path, projdir, 'workspace', 'load_data_csv', batchname, p) for p in plates]

plates = [i.split("/")[-1].split("__")[0] for i in fpath][0]


fimages = fimages[0]


lst = []

for i, image in enumerate(os.listdir(ppath)):
    
    imgpath = os.path.join(ppath, image)
    
    if i==2:
        
        print(imgpath)
        break
    
#     if imagpath.endswith("tiff"):
        
#         head, tail = os.path.split(imagpath)
        
#         lst.append(tail)


channels = {'ch1':"OrigMito",
'ch2':"OrigAGP",
'ch3':"OrigRNA",
'ch4':"OrigER",
'ch5':"OrigDNA",
"ch6": "OrigHighZBF",
'ch7': "OrigLowZBF",
"ch8":"OrigBrightfield"}

keys = list(channels.keys())
values = list(channels.values())


lst = ['r01c01f01p01-ch1sk6fk1fl1.tiff', 'r01c01f01p01-ch2sk6fk1fl1.tiff', 
'r01c01f01p01-ch3sk6fk1fl1.tiff', 'r01c01f01p01-ch4sk6fk1fl1.tiff', 
'r01c01f01p01-ch5sk6fk1fl1.tiff', 'r01c01f01p01-ch6sk6fk1fl1.tiff', 
'r01c01f01p01-ch7sk7fk1fl1.tiff', 'r01c01f01p01-ch8sk6fk1fl1.tiff']




ch1 = [s for s in lst if 'ch1' in s]
ch2 = [s for s in lst if 'ch2' in s]
ch3 = [s for s in lst if 'ch3' in s]
ch4 = [s for s in lst if 'ch4' in s]
ch5 = [s for s in lst if 'ch5' in s]
ch6 = [s for s in lst if 'ch6' in s]
ch7 = [s for s in lst if 'ch7' in s]
ch8 = [s for s in lst if 'ch8' in s]



zippedlist = list(zip(ch1, ch2, ch3, ch4, ch5, ch6, ch7, ch8))

df = pd.DataFrame(zippedlist, columns=["FileName_"+chname for chname in values])

df = pd.concat([df, pd.DataFrame(columns=["PathName_"+chname for chname in values])])

df[["PathName_"+chname for chname in values]] = fimages

wellname = df['FileName_OrigDNA'].tolist()

pattern = re.compile("r(?P<row>\d+)c(?P<column>\d+)f(?P<field>\d+)p(?P<site>\d+)-ch(?P<channelnumber>\d+)")


## apply this regrex to all the imagelist

match = [pattern.match(i) for i in wellname]
row = [r.group("row") for r in match]
col= [c.group("column") for c in match]
field= [f.group("field") for f in match]
site= [int(s.group("site")) for s in match]
channel= [ch.group("channelnumber") for ch in match]

## Defining Well names

rc = [r+c for r, c in zip(row, col)]

well_assignment= {'01' : "A",'02': "B",'03':"C",'04':"D",
                  '05': "E",'06':"F",'07':"G",'08':"H",
                  '09':"I",'10':"J",'11':"K",'12':"L",
                  '13':"M",'14':"N",'15':"O",'16':"P"
}

well = [well_assignment.get(i[0:2])+i[2:] for i in rc]

df['Metadata_Well'] = well
df['Metadata_Site'] = site
df['Metadata_Plate'] = plates




