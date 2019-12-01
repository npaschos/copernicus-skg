import pickle
import numpy as np

def pickle2data(name):

    fl_name_lat = name + '.lat.pkl'
    fl_name_long = name + '.long.pkl'
    fl_name_val = name + '.val.pkl'
    
    with open(fl_name_lat, 'rb') as fl:
        lat = pickle.load(fl)
    
    with open(fl_name_long, 'rb') as fl:
        lon = pickle.load(fl)

    with open(fl_name_val, 'rb') as fl:
        val = pickle.load(fl)


    return lat, lon, val

def data2airQ():

    no2_lat, no2_lon, no2_val = pickle2data('no2')
    o3_lat, o3_lon, o3_val = pickle2data('o3')
    pm10_lat, pm10_lon, pm10_val = pickle2data('pm10')
    pm25_lat, pm25_lon, pm25_val = pickle2data('pm25')

    # Area of interest calculated in a box 
    box_lat_x1 = 50.15 #50.1 
    box_lat_x2 = 49.95 # 49.8 
    box_lon_y1 = 8.47 #8.4 - 8.45
    box_lon_y2 = 8.95 #9.0 - 9.05

    # Need automation here
    # index_lat_x1 = np.where(no2_lat== box_lat_x1)
    index_lat_x1 = 108
    index_lat_x2 = 111
    index_lon_y1 = 198
    index_lon_y2 = 204


    no2_index = list()
    o3_index = list()
    pm25_index = list()
    pm10_index = list()

    for i in range(index_lat_x1, index_lat_x2 + 1):
        for j in range(index_lon_y1, index_lon_y2 + 1):
            no2_index.append(no2_val[i][j]) 
            o3_index.append(o3_val[i][j])
            pm25_index.append(pm25_val[i][j])
            pm10_index.append(pm10_val[i][j])

    no2_index_norm = list()
    o3_index_norm = list()
    pm25_index_norm = list()
    pm10_index_norm = list()
   
    for i in range (len(no2_index)):
        if no2_index[i] > 0 and no2_index[i] <= 50:
            no2_index_norm.append((25 - 0)*(no2_index[i] - 0)/(50 - 0) + 0)
        elif no2_index[i] > 50 and no2_index[i] <= 100:
            no2_index_norm.append((50 - 25)*(no2_index[i] - 50)/(100 - 50) + 25)
        elif no2_index[i] > 100 and no2_index[i] <= 200:
            no2_index_norm.append((75 - 50)*(no2_index[i] - 100)/(200 - 100) + 50)
        elif no2_index[i] > 200 and no2_index[i] <= 400:
            no2_index_norm.append((100 - 75)*(no2_index[i] - 200)/(400 - 200) + 75)
        else:
            no2_index_norm.append(101)

        if o3_index[i] > 0 and o3_index[i] <= 60:
            o3_index_norm.append((25 - 0)*(o3_index[i] - 0)/(60 - 0) + 0)
        elif o3_index[i] > 60 and o3_index[i] <= 120:
            o3_index_norm.append((50 - 25)*(o3_index[i] - 60)/(120 - 60) + 25)
        elif o3_index[i] > 120 and o3_index[i] <= 180:
            o3_index_norm.append((75 - 50)*(o3_index[i] - 120)/(180 - 120) + 50)
        elif o3_index[i] > 180 and o3_index[i] <= 240:
            o3_index_norm.append((100 - 75)*(o3_index[i] - 180)/(240 - 180) +75)
        else:
            o3_index_norm.append(101)

        if pm25_index[i] > 0 and pm25_index[i] <= 15:
            pm25_index_norm.append((25 - 0)*(pm25_index[i] - 0)/(15 - 0) + 0)
        elif pm25_index[i] > 15 and pm25_index[i] <= 30:
            pm25_index_norm.append((50 - 25)*(pm25_index[i] - 15)/(30 - 15) + 25)
        elif pm25_index[i] > 30 and pm25_index[i] <= 55:
            pm25_index_norm.append((75 - 50)*(pm25_index[i] - 30)/(55 - 30) + 50)
        elif pm25_index[i] > 55 and pm25_index[i] <= 100:
            pm25_index_norm.append((100 - 75)*(pm25_index[i] - 55)/(100 - 55) + 75)
        else:
            pm25_index_norm.append(101)

        if pm10_index[i] > 0 and pm10_index[i] <= 25:
            pm10_index_norm.append((25 - 0)*(pm10_index[i] - 0)/(25 - 0) + 0)
        elif pm10_index[i] > 25 and pm10_index[i] <= 50:
            pm10_index_norm.append((25 - 0)*(pm10_index[i] - 25)/(50 - 25) + 25)
        elif pm10_index[i] > 50 and pm10_index[i] <= 90:
            pm10_index_norm.append((25 - 0)*(pm10_index[i] - 50)/(90 - 50) + 50)
        elif pm10_index[i] > 90 and pm10_index[i] <= 180:
            pm10_index_norm.append((25 - 0)*(pm10_index[i] - 90)/(180 - 90) + 75)
        else:
            pm10_index_norm.append(101)

    air_q = list()
    for i in range (len(no2_index_norm)):
        alist = [pm10_index_norm[i],pm25_index_norm[i], o3_index_norm[i], no2_index_norm[i], no2_index_norm[i], no2_index_norm[i]]
        air_q.append(min(alist))

    air_q = np.reshape(air_q,(4,7))
    
    return air_q