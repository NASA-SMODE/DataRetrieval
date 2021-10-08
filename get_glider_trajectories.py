import numpy as np
import xarray as xr
from siphon.catalog import TDSCatalog

# Settings 
ids = ['ng231','ng258','ng268','ng316',
       'ng350','ng533','ng599','ng665',
       'ng734','ng780']

base_url = 'http://smode.whoi.edu:8080/thredds/dodsC/insitu/navo_glider/'
cat = TDSCatalog('http://smode.whoi.edu:8080/thredds/catalog/insitu/navo_glider/catalog.html')

# Get filelist and build list of datapaths

filelist=[file for file in 
            cat.datasets if file.startswith(ids[0])]

datapath_nooptics = [base_url+file for file in 
                        filelist if 'optics' not in file]

# Get averaged earth coordinates of glider profiles

lat, lon = np.array([]), np.array([])

# Data time is epoch time: since 00:00Z 1 January 1970
start =  np.datetime64('1970-01-01') 
time = []

for path in datapath_nooptics:
    
    glider_data = xr.open_dataset(path)
  
    lat = np.hstack([lat, glider_data.latitude.mean().values])
    lon = np.hstack([lon, glider_data.longitude.mean().values])
    time.append(glider_data.scitime.mean().values + start)

time = np.array(time)

# TODO: loop over gliders and put the data in a json file

# if __name__ == "__main__":
#     main()