#!/usr/bin/env python

"""
Extracting ztf.alert.candidate fields from avro packets
collected as a tar.gz file and writing them into a csv file.

Please check the packet contents at:
https://zwickytransientfacility.github.io/ztf-avro-alert/schema.html
    
Note:
    if remove_duplicates = True (default)
    then remove all rows with dubplicates 
    from .csv file.

Command line to run the code:
python avro_csv.py ztf_public_20180601         # "20180601" is just an example.  

Output:
    ztf_public_20180601.csv
    
    log.txt file containing the following info:
    20180601,# of alerts before checking for duplicates,# of alerts after removing duplicates.
  
"""

import os
import sys
import csv
import pandas as pd
import numpy as np
import argparse
import tarfile
import fastavro

remove_duplicates = True

# set the path to directory containing "ztf_public_[date].tar.gz" file on your local machine.
pth = '/astro/ztf_avro_alerts/'

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
                    #pac2.pop('pdiffimfilename',0), pac2.pop('programid',0)
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

            with open(pth+'log.txt','a') as lg:
                lg.write('%s,%i,%i\n'%
                         (args.topic.split('_')[2], df_bf, df_af))

            df.to_csv(pth+args.topic+'.csv', sep=',', header=True, index=False)


        tar.close()

    else:
        print('filename does not exist to read! \n')
        with open(pth+'log.txt','a') as lg:
            lg.write('%s,%i,%i\n'%(args.topic.split('_')[2], 0, 0) )


if __name__ == "__main__":
    main()
    
