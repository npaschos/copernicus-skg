import math
import numpy
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.cm import hot
from PIL import Image

from util import read_grib
from data_processing import data2airQ

img = Image.open('frankfurt.png')
era_hourly = read_grib('era5-0000-1200.grib')
skin_ds = read_grib('skin.grib')

# get data of interest
night_datay = era_hourly.data_vars['t2m'].values[0][399:403]
frankfurt_night = list()
for lat in night_datay:
    frankfurt_night.append(lat[84:91])

night_avg = numpy.average(frankfurt_night)
night_datay = None

day_datay = era_hourly.data_vars['t2m'].values[1][399:403]
frankfurt_day = list()
for lat in day_datay:
    frankfurt_day.append(lat[84:91])

day_avg = numpy.average(frankfurt_day)
day_datay = None

skin_datay = skin_ds.data_vars['skt'].values[399:403]
frankfurt_skin = list()
for lat in skin_datay:
    frankfurt_skin.append(lat[84:91])

skin_min = numpy.min(frankfurt_skin)
skin_max = numpy.max(frankfurt_skin)
skin_datay = None

frankfurt_day = frankfurt_day - day_avg
frankfurt_night = frankfurt_night - night_avg

frankfurt_hourly = 0.65 * frankfurt_night + 0.35 * frankfurt_day
frankfurt_hourly_norm = list()
frankfurt_skin_norm = (100 - 0) / (skin_max - skin_min) * (frankfurt_skin -
                                                           skin_min)

frankfurt_hourly = frankfurt_hourly.reshape((28))
for i in range(len(frankfurt_hourly)):
    if frankfurt_hourly[i] > 0 and frankfurt_hourly[i] <= 1:
        frankfurt_hourly_norm.append((25 - 0) * (frankfurt_hourly[i] - 0) /
                                     (1 - 0) + 0)
    elif frankfurt_hourly[i] > 1 and frankfurt_hourly[i] <= 3:
        frankfurt_hourly_norm.append((50 - 25) * (frankfurt_hourly[i] - 1) /
                                     (3 - 1) + 25)
    elif frankfurt_hourly[i] > 3 and frankfurt_hourly[i] <= 5:
        frankfurt_hourly_norm.append((75 - 50) * (frankfurt_hourly[i] - 3) /
                                     (5 - 3) + 50)
    elif frankfurt_hourly[i] > 5 and frankfurt_hourly[i] <= 12:
        frankfurt_hourly_norm.append((100 - 75) * (frankfurt_hourly[i] - 5) /
                                     (12 - 5) + 75)
    else:
        frankfurt_hourly_norm.append(101)

frankfurt_hourly_norm = numpy.reshape(frankfurt_hourly_norm, (4, 7))

air_q = data2airQ()

# total_frankfurt = (frankfurt_hourly_norm + air_q) / 2
total_frankfurt = (frankfurt_hourly_norm + air_q) * 0.4 + 0.2 * frankfurt_skin_norm

# https://seaborn.pydata.org/tutorial/color_palettes.html
# sns.color_palette("RdBu_r", 7)
# sns.color_palette("coolwarm", 7)
hmax = sns.heatmap(
    total_frankfurt,
    # cmap=hot,
    cmap=sns.color_palette("RdBu_r", 7),
    alpha=0.5,  # whole heatmap is translucent
    annot=False,
    zorder=2,
)
# plt.show()

hmax.imshow(img,
            aspect=hmax.get_aspect(),
            extent=hmax.get_xlim() + hmax.get_ylim(),
            zorder=1)  #put the map under the heatmap

plt.show()
