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
import shutil
import zipfile
import os
import datetime
import glob
outdata = 'corona_data/COVID-19-master/csse_covid_19_data/csse_covid_19_time_series/'
outdata2 = 'corona_data/output/'

# shutil.rmtree("corona_data/COVID-19-master")
# url='https://codeload.github.com/CSSEGISandData/COVID-19/zip/master'
# response = requests.get(url)
# with open(os.path.join("corona_data", "COVID-19-master.zip"), 'wb') as f:
#     f.write(response.content)
# with zipfile.ZipFile('corona_data/COVID-19-master.zip', 'r') as zip_ref:
#     zip_ref.extractall('corona_data')

rd = pd.read_csv(outdata+'time_series_19-covid-Deaths.csv')
rename = rd.rename(columns={"Country/Region":"Country" , "Province/State":"Province"})
sel_data = rename.query('Country == "Thailand"')
drop_cl = sel_data.drop(columns=['Country','Province', 'Lat', 'Long'])
#rr = pd.melt(rd2, value_vars=['1/22/20', '1/23/20'])
rows = drop_cl.melt(id_vars=[], 
        var_name="Date", 
        value_name="Value")
ab = len(rows) - 1
#print(rows[ab:])
corona_th = (rows[1:])
corona_th.to_json(outdata2+"deaths_th.json", orient = "records", date_format = "epoch", double_precision = 10, force_ascii = False, date_unit = "ms", default_handler = None)
corona_th_day = (rows[ab:])
corona_th_day.to_json(outdata2+"deaths_th_day.json", orient = "records", date_format = "epoch", double_precision = 10, force_ascii = False, date_unit = "ms", default_handler = None)

point_sel = rename.iloc[:, list(range(4)) + [-1]]
point_sel2 = point_sel.rename(columns={point_sel.columns[-1]:"total"})
point_sel2.to_csv(outdata2+'all_data_deaths.csv')
#create xy
rd2 = pd.read_csv(outdata2+'all_data_deaths.csv')
geometry = [Point(xy) for xy in zip(rd2['Long'], rd2['Lat'])]
crs = {'init': 'epsg:4326'}
gdf = gpd.GeoDataFrame(rd2, crs=crs, geometry=geometry)
gdf.to_file(outdata2+'corona_deaths.shp' , encoding = 'utf-8')