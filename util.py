import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt


def generate_earth_image(x0=0, x1=359, y0=-90, y1=90):
    fig = plt.figure()

    ax = fig.add_subplot(projection=ccrs.PlateCarree())
    ax.set_extent([x0, x1, y0, y1], crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.LAKES, alpha=0.5)
    ax.add_feature(cfeature.RIVERS)
    # fig.savefig('map.png')
    plt.show()


def read_grib(infile='era5.grib'):
    '''
		load the data in xarray format
	'''
    return xr.open_dataset(infile, engine='cfgrib')
