from PIL import Image
from pathlib import Path
import argparse
import glob
import os
import pandas as pd
from re import search
import re



path = '/home/ubuntu/bucket/projects'
projdir = '2019_07_11_JUMP-CP-pilots'
batchname = '2021_02_26_Stain5_CondC_Thermo_Standard'
outpath = os.path.join(path, projdir, 'workspace', 'load_data_csv', batchname, plates)


def load_data():
    
    lst=[]

    for i, image in enumerate(os.listdir(fpath)):

        imgpath = os.path.join(fpath, image)

        if imgpath.endswith("tiff"):

            head, tail = os.path.split(imgpath)

            lst.append(tail)
            
            
    channels = {'ch1':"OrigDNA",
    'ch2':"OrigER",
    'ch3':"OrigRNA",
    'ch4':"OrigAGP",
    'ch5':"OrigMito",
    }

    keys = list(channels.keys())
    values = list(channels.values())


    ch1 = [s for s in lst if 'ch1' in s]
    ch2 = [s for s in lst if 'ch2' in s]
    ch3 = [s for s in lst if 'ch3' in s]
    ch4 = [s for s in lst if 'ch4' in s]
    ch5 = [s for s in lst if 'ch5' in s]
    

    zippedlist = list(zip(ch1, ch2, ch3, ch4, ch5))

    df = pd.DataFrame(zippedlist, columns=["FileName_"+chname for chname in values])

    path_columns = { c : fpath for c in ["PathName_"+chname for chname in values]}

    df = df.assign(**path_columns)


    wellname = df['FileName_OrigDNA'].tolist()


    pattern = re.compile("r(?P<row>\d+)c(?P<column>\d+)f(?P<site>\d+)p(?P<zplane>\d+)-ch(?P<channelnumber>\d+)")


    ## apply this regrex to all the imagelist

    match = [pattern.match(i) for i in wellname]
    row = [r.group("row") for r in match]
    col= [c.group("column") for c in match]
    site= [f.group("site") for f in match]
    zplane= [int(s.group("zplane")) for s in match]
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
    df['Metadata_ZPlane'] = zplane
    
    colnames = ['FileName_OrigDNA', 'PathName_OrigDNA',
             'FileName_OrigER', 'PathName_OrigER',
             'FileName_OrigRNA', 'PathName_OrigRNA',
             'FileName_OrigAGP', 'PathName_OrigAGP', 
             'FileName_OrigMito', 'PathName_OrigMito',
             'Metadata_Plate','Metadata_Well', 
            'Metadata_Site','Metadata_ZPlane']
    
    
    return df.reindex(columns=colnames)




def load_data_with_illum(*args):

    df['FileName_IllumDNA'] = plates+'_IllumDNA.npy'
    
    df['PathName_IllumDNA'] = os.path.join(batchpath, 'illum', plates)
    
    df['FileName_IllumER'] = plates+'_IllumER.npy'
    
    df['PathName_IllumER'] = os.path.join(batchpath, 'illum', plates)
    
    df['FileName_IllumRNA'] = plates+'_IllumRNA.npy'
    
    df['PathName_IllumRNA'] = os.path.join(batchpath, 'illum', plates)
    
    df['FileName_IllumAGP'] = plates+'_IllumAGP.npy'
    
    df['PathName_IllumAGP'] = os.path.join(batchpath, 'illum', plates)
    
    df['FileName_IllumMito'] = plates+'_IllumMito.npy'
    
    df['PathName_IllumMito'] = os.path.join(batchpath, 'illum', plates)

    colnames = ['FileName_OrigDNA', 'PathName_OrigDNA',
                 'FileName_OrigER', 'PathName_OrigER',
                 'FileName_OrigRNA', 'PathName_OrigRNA',
                 'FileName_OrigAGP', 'PathName_OrigAGP', 
                 'FileName_OrigMito', 'PathName_OrigMito',
                 'Metadata_Plate','Metadata_Well', 
                'Metadata_Site', 'Metadata_ZPlane','FileName_IllumDNA', 'PathName_IllumDNA', 
                'FileName_IllumER', 'PathName_IllumER', 
                'FileName_IllumRNA', 'PathName_IllumRNA',
                'FileName_IllumAGP', 'PathName_IllumAGP',
                'FileName_IllumMito', 'PathName_IllumMito']
    
    return df.reindex(columns=colnames)






def main(*args):
    
    plist = [f for f in os.listdir(os.path.join(path, projdir, batchname, 'images'))]

    for p in plist:

        fpath = os.path.join(path, projdir, batchname, 'images', p, 'Images')

        plates = fpath.split('/')[-2].split('__')[0]

        outpath = os.path.join(path, projdir, 'workspace', 'load_data_csv', batchname, plates)


        def makedirectory():

            try:
                os.makedirs(outpath)
                
                print("Directory", outpath, "is created")
                
            except IOError:
                
                print("Directory", outpath, "already exists")

        directory = makedirectory()

        df = load_data() ## Applying function

        df.to_csv(outpath + "/" + 'load_data.csv', index=False)

        loaddataillum = load_data_with_illum(*loaddata)

        loaddataillum.to_csv(outpath + "/" + 'load_data_with_illum.csv')
        
        
    
    return

    
main(path, projdir, batchname)




