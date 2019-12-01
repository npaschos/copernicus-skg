# requires pip3 install cdsapi
# then create $(HOME)/.cdsapirc containing the credentials
# differnet ToS must be accepted depending on the requests dataset

import cdsapi
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--outfile', '-of', type=str, default='download')
parser.add_argument('--dataset',
                    '-d',
                    type=str,
                    default='reanalysis-era5-land-monthly-means')
parser.add_argument('--format', '-f', type=str, default='grib')

args = parser.parse_args()

c = cdsapi.Client()

outfile_name = '{}.{}'.format(args.outfile, args.format)
dataset_options = {
    'format': args.format,
    'variable': ['skin_temperature'],
    'product_type': 'monthly_averaged_reanalysis',
    'time': '00:00',
    'year': '2019',
    'month': '04'
}

options = {
        'format':'grib',
        'product_type':'monthly_averaged_reanalysis',
        'variable':[
            '2m_dewpoint_temperature','2m_temperature','forecast_albedo',
            'skin_temperature'
        ],
        'year':'2019',
        'month':'04',
        'time':'00:00'
}

c.retrieve(args.dataset, options, outfile_name)
