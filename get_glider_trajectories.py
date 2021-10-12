import numpy as np
import xarray as xr
from siphon.catalog import TDSCatalog

def main():

    # Settings 
    ids = ['ng231','ng258','ng268','ng316',
        'ng350','ng533','ng599','ng665',
        'ng734','ng780']

    base_url = 'http://smode.whoi.edu:8080/thredds/dodsC/insitu/navo_glider/'
    cat = TDSCatalog('http://smode.whoi.edu:8080/thredds/catalog/insitu/navo_glider/catalog.html')

    # Loop over gliders and get averaged earth coordinates
    for id in ids:

        # Get filelist and build list of datapaths
        filelist=[file for file in 
                    cat.datasets if file.startswith(id)]

        datapath_nooptics = [base_url+file for file in 
                                filelist if 'optics' not in file]

        lat, lon = np.array([]), np.array([])

        # scitime = timedelta from 000Z 1/1/1970
        start =  np.datetime64('1970-01-01') - np.timedelta64(1,'D')
        time = []

        for path in sorted(datapath_nooptics):
            
            glider_data = xr.open_dataset(path)
        
            # Average coordinates
            lat = np.hstack([lat, glider_data.latitude.mean().values])
            lon = np.hstack([lon, glider_data.longitude.mean().values])
            time.append(glider_data.scitime.mean().values + start)

        # round time at the minute level
        time = np.array(time).astype('datetime64[m]')   

        # mask bad data
        lon[lon>360] = np.nan
        lat[lon>360] = np.nan 
    
        # put data into a Dataset
        coordinates = {
            'time': time, 
            'glider': id
        } 
        variables = {
            'longitude': ('time', lon),
            'latitude': ('time', lat)
        } 

        ds = xr.Dataset(variables, coords=coordinates
                    ).expand_dims('glider')

        if id is ids[0]:
            glider_trajectories = ds 
        else: 
            glider_trajectories = xr.merge([glider_trajectories,ds])

        # save trajectories to netCDF file
        glider_trajectories.to_netcdf('output/glider_trajectories.nc')

if __name__ == "__main__":
    main()