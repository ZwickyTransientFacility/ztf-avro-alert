#!/usr/bin/env python

"""
Extracting the following info from avro files
collected as a tar file and writing them into a csv file.

Note:
    if remove_duplicates = True (default)
    then remove all rows with dubplicates 
    from .csv file.
    
    
Write number of alerts in a given topic into logMSIPSummary.txt file. 
    format: # of alerts before checking for duplicates, # of alerts after removing duplicates,
            min('candid'), max('candid'), min('jd'), max('jd') 
    
"""

import os
import sys
import csv
import pandas as pd
import numpy as np
import argparse
import tarfile
import fastavro
#from glob import glob

remove_duplicates = True

# chnage the following path to where you want to dump generated files.
pth = '/epyc/data/ztfMSIP/'

pth2 = '/epyc/data/ztfDB/'

alert_fields = 'objectId,jd,fid,pid,diffmaglim,pdiffimfilename,programpi,programid,candid,isdiffpos,tblid,nid,rcid,field,xpos,ypos,\
ra,dec,magpsf,sigmapsf,chipsf,magap,sigmagap,distnr,magnr,sigmagnr,chinr,sharpnr,sky,magdiff,\
fwhm,classtar,mindtoedge,magfromlim,seeratio,aimage,bimage,aimagerat,bimagerat,elong,nneg,nbad,rb,ssdistnr,\
ssmagnr,ssnamenr,sumrat,magapbig,sigmagapbig,ranr,decnr,sgmag1,srmag1,simag1,szmag1,sgscore1,distpsnr1,ndethist,ncovhist,\
jdstarthist,jdendhist,scorr,tooflag,objectidps1,objectidps2,sgmag2,srmag2,simag2,szmag2,sgscore2,distpsnr2,objectidps3,sgmag3,\
srmag3,simag3,szmag3,sgscore3,distpsnr3,nmtchps,rfid,jdstartref,jdendref,nframesref'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('topic', type=str,
                        help='Name of tar file to open and extract info.')

    args = parser.parse_args()

    if (tarfile.is_tarfile(pth+args.topic+'.tar.gz')):
        tar = tarfile.open(pth+args.topic+'.tar.gz','r:gz')  # <-- if tar.gz
        #tar = tarfile.open(pth+args.topic+'.tar','r')         # <-- if .tar

        with open(pth+args.topic+'.csv','w') as alert_packet:

            alert_packet.write('%s\n'%alert_fields)

            for member in tar.getmembers():

                fle = tar.extractfile(member)
                freader = fastavro.reader(fle)
                schema = freader.schema

                for packet in freader:

                    pac1 = {}
                    pac1['objectId'] = packet['objectId']
                    pac2 = packet['candidate']
                    # remove any field from packet you're not interested using the following commented out line.
                    #pac2.pop('pdiffimfilename',0), pac2.pop('programpi',0)
                    pac = {**pac1, **pac2}
                    keys = pac.keys()
                    dict_writer = csv.DictWriter(alert_packet, keys)
                    dict_writer.writerow(pac)


        if remove_duplicates:

            df = pd.read_csv(pth+args.topic+'.csv', delimiter=',', low_memory=False)
            df_bf = len(df)
            #
            df.drop_duplicates(subset=None, inplace=True)
            df_af = len(df)

            with open(pth2+'logMSIPSummary.txt','a') as lg:
                lg.write('%s \t %i \t %i \t %i \t %i \t %.9f \t %.9f \n'%
                         (args.topic.split('_')[2], df_bf, df_af, min(df['candid']), max(df['candid']), min(df['jd']), max(df['jd']) ))

            df.to_csv(pth+args.topic+'.csv', sep=',', header=True, index=False)


        tar.close()

    else:
        print('filename does not exist to read! \n')
        with open(pth2+'logMSIPSummary.txt','a') as lg:
            lg.write('%s \t %i \t %i \t %i \t %i \t %.9f \t %.9f \n'%(args.topic.split('_')[2], 0, 0, 0, 0, 0, 0) )


if __name__ == "__main__":
    main()

       
