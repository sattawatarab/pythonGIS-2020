# -*- coding: utf-8 -*-
##########################################
# By : Sattawat Arab : GIS Analyst and Backend Engineer
######## © I-Bitz Company Limited. ########

import pandas as pd
import geopandas as gpd
import pyodbc 
import requests
from datetime import datetime
from datetime import timedelta 
from shapely.geometry import Point
import geojson
import shutil as cp
import os
import datetime
import glob

outdata = 'rcs/'
now = datetime.datetime.now()
yy = now.year
provid = 'ภก'
cnt = 4
url = "http://www.thairsc.com/services/GetAmphurTopThreeList"
for cnt in range(1,cnt):
    querystring = {"provid":provid,"ampid":cnt,"years":yy} 
    headers = {
        }
    #print(querystring)
    response = requests.request("POST", url, headers=headers, params=querystring)
    Output = response.json()
    #print(Output['dtLatlng'])
    dict1 =Output
    #print(Output)
    ab0 = len(Output['dtLatlng'])
    if ab0 == 0:
        print("can not connect api")
    elif ab0 > 0:
        df0 = pd.DataFrame()
        list_branch_accdate=[]
        for i in range(0,ab0):
            list_branch_accdate.append(dict1['dtLatlng'][i]['accdate'])
        df0['accdate']=list_branch_accdate
        list_branch_accplace=[]
        for i in range(0,ab0):
            list_branch_accplace.append(dict1['dtLatlng'][i]['accplace'])
        df0['accplace']=list_branch_accplace

        list_branch_accnature=[]
        for i in range(0,ab0):
            list_branch_accnature.append(dict1['dtLatlng'][i]['accnature'])
        df0['accnature']=list_branch_accnature

        list_branch_isdead=[]
        for i in range(0,ab0):
            list_branch_isdead.append(dict1['dtLatlng'][i]['isdead'])
        df0['isdead']=list_branch_isdead

        list_branch_lat=[]
        for i in range(0,ab0):
            list_branch_lat.append(dict1['dtLatlng'][i]['lat'])
        df0['lat']=list_branch_lat

        list_branch_lng=[]
        for i in range(0,ab0):
            list_branch_lng.append(dict1['dtLatlng'][i]['lng'])
        df0['lng']=list_branch_lng
        df0.to_csv(outdata+'outdata/'+provid+str(cnt)+'.csv')

extension = 'csv'
all_filenames = [i for i in glob.glob(outdata+'outdata/'+provid+'*.{}'.format(extension))]
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
combined_csv.to_csv(outdata+'sumdata/'+provid+"combined_csv_pk-2018.csv", index=False, encoding='utf-8-sig')