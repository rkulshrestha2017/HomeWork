
# WeatherPy - Analysis

### Summary of Data and Rationale
    
  + For this project, 3 different sets of data were pulled into one data frame, the current weather at time of request, the weather at the highest temperature forecasted at three hour intervals in the next 24 hours from time of request, and the average of the selected weather parameters forecasted in intervals of 3 hours for the next 5 days (120 hours) from time of request.
    
  + Initially, the hypotheses was that current weather would give you skewed information based on longitude and time of day, while the forecasted weather may not be as accurate.  The belief was that pulling information only from the forecasted maximized temperature over a 24 hours period would minimize this effect, but also might skew additional parameters like cloud cover and wind speed.  Surprisingly, no noticeable difference was experienced between these two groups.
        
  + The average values over the next 5 days/120h hours did yield slightly different results, but might not allow us to inspect addition relationships accurately.  For example, to inspect temperature versus wind speed exact data points may be more beneficial than the average values.  This information, however, may not be as accurate as current data or a 24 hours forecast.


        
### Analysis
    
   + Using 24 hour data, we can see that cities on or very near the equator did not experience the highest temperatures, although high temperatures were more consistent in that area and there was slightly less variability.  The highest temperatures where instead experienced closer to the Tropics of Cancer and Capricorn, located at 23.5 and -23.5 degrees latitude respectively.  This phenomenon and variability may be due to the differences in the number of cities that fall along these latitudes as well as the geographic features.  For example, the Sahara Desert falls along the Tropic of Cancer (see graphs at the end of document).   Instead, it is safer to conclude that the highest temperatures were experienced between latitudes of -30 and 30 degrees, although with generally more variability as you increase distance from 0 degrees latitude.  Using the average temperature parameter, we can see more consistency between -20 and 20 degrees latitude.  
    
    Percent humidity doesn't seem to have much correlation to latitude.  Several varying latitudes have % humidity ranging from 40 to 100%.  However, based on this small date sampling, humidity does experience variation as we approach the Tropic of Cancer and Capricorn with some falling below 40% humidity.  The cities on the equator experienced the 40% to 100% range. No significant correlation was found between latitude and cloud cover or wind speed.  Frequency of wind speed, however, can be observed.  The most common observation was speeds between 0 and 10 mph.  Observations decrease in frequency as you increase wind speed with rare occurrences of wind speeds greater than 30 mph.

 
### Additional Notes
    
 + By plotting latitude versus longitude, we can observe addition patterns in weather by location.  For example, local patterns are observed by geographic regions.  For example, humidity and wind speed appear to be generally higher in coastal regions when compared to inland regions.
 
 + This dataset is limited by the sampling time span.  Historical data might give a better picture of trends and allow you to explore additional relationships.



```python
import numpy as np
import pandas as pd
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns
import requests as req
from citipy import citipy
import unidecode
import time
from math import sqrt
from datetime import datetime
```


```python
#api_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath('__file__'))))))
file_name = os.path.join("Keys/api_keys.json")
data = json.load(open(file_name))

gkey = data['google_places_api_key']
wkey = data['open_weather_api_key']
```


```python
# Build data frame of randomly generated lat and long
location_data = pd.DataFrame()
location_data['rand_lat'] = [np.random.uniform(-90,90) for x in range(1500)]
location_data['rand_lng'] = [np.random.uniform(-180, 180) for x in range(1500)]

# add closest city and country column
location_data['closest_city'] = ""
location_data['country'] = ""

#find and add closest city and country code
for index, row in location_data.iterrows():
    lat = row['rand_lat']
    lng = row['rand_lng']
    location_data.set_value(index, 'closest_city', citipy.nearest_city(lat, lng).city_name)
    location_data.set_value(index, 'country', citipy.nearest_city(lat, lng).country_code)
```


```python
# delete repeated cities and find unique city count
location_data = location_data.drop_duplicates(['closest_city', 'country'])
location_data = location_data.dropna()
len(location_data['closest_city'].value_counts())
```




    600




```python
# USE BELOW VALUE FOR COUNT MATCHING 
rec_check = len(location_data['closest_city'])  #Difference is due to same city name but different country
rec_check
```




    603




```python
#preview data
location_data.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>rand_lat</th>
      <th>rand_lng</th>
      <th>closest_city</th>
      <th>country</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>26.122719</td>
      <td>4.735868</td>
      <td>adrar</td>
      <td>dz</td>
    </tr>
    <tr>
      <th>1</th>
      <td>85.980760</td>
      <td>-148.899985</td>
      <td>barrow</td>
      <td>us</td>
    </tr>
    <tr>
      <th>2</th>
      <td>61.037508</td>
      <td>-146.631758</td>
      <td>palmer</td>
      <td>us</td>
    </tr>
    <tr>
      <th>3</th>
      <td>-55.549424</td>
      <td>-97.616707</td>
      <td>punta arenas</td>
      <td>cl</td>
    </tr>
    <tr>
      <th>4</th>
      <td>-2.930857</td>
      <td>-44.233272</td>
      <td>rosario</td>
      <td>br</td>
    </tr>
  </tbody>
</table>
</div>




```python
# keep only city and country
# random lats and lngs no longer needed
location_data = location_data[['closest_city', 'country']]

#rename columnds for later merging
location_data = location_data.rename(columns = {'closest_city': 'city'})
```


```python
# read in open weather map's country Id json
# downloaded from https://openweathermap.org/appid#work
# done because of open weather maps documentation suggestion

api_city_data = pd.read_json('city.list.json')

for index, row in api_city_data.iterrows():
    lower_city = row['name'].lower() #make all city name lowercase
    unaccented = unidecode.unidecode(lower_city) # strip accents from city name
    lower_country = row['country'].lower() # make all two digit county 
    api_city_data.set_value(index, 'name', unaccented) # reset the value of name (city) to stripped down version
    api_city_data.set_value(index, 'country', lower_country) # reset the value of country to lower case
    
api_city_data = api_city_data.rename(columns = {'name': 'city'}) # rename for merge 
```


```python
#merge with random cities from location_data

merged_df = location_data.merge(api_city_data, how = 'left', on = ('city', 'country'))
merged_df = merged_df.drop_duplicates(['city', 'country'])

# to verify with number below
len(merged_df)
```




    603




```python
#check with above
rec_check
```




    603




```python
#preview merged_df
merged_df.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>city</th>
      <th>country</th>
      <th>coord</th>
      <th>id</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>adrar</td>
      <td>dz</td>
      <td>{'lon': -0.29388000000000003, 'lat': 27.87429}</td>
      <td>2508813.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>barrow</td>
      <td>us</td>
      <td>{'lon': -156.788727, 'lat': 71.290581}</td>
      <td>5880054.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>palmer</td>
      <td>us</td>
      <td>{'lon': -98.257294, 'lat': 41.22224}</td>
      <td>5074769.0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>punta arenas</td>
      <td>cl</td>
      <td>{'lon': -70.916672, 'lat': -53.150002}</td>
      <td>3874787.0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>rosario</td>
      <td>br</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>




```python
#clean-up
merged_df['coord'] = merged_df['coord'].fillna('') #fill na cells with emplty string for coordinates
merged_df['id'] = merged_df['id'].fillna(0) # fill na with 0 for id in order to change to int64
merged_df['id'] = merged_df['id'].astype(dtype = 'int64') # cast id column as type int64 to remove floating .0
merged_df['id'].dtype #check type of id
```




    dtype('int64')




```python
#check how many returned valid ids
merged_df['id'].value_counts() 
```




    0          94
    5380437     1
    7294638     1
    3893629     1
    5906757     1
    3573062     1
    6357322     1
    3402648     1
    1272140     1
    304922      1
    1490256     1
    1648186     1
    1028434     1
    2027859     1
    1635882     1
    2456917     1
    1529484     1
    687449      1
    1154689     1
    1503037     1
    3424607     1
    3466594     1
    5095779     1
    779622      1
    2122104     1
    3932145     1
    1516905     1
    2122090     1
    3651949     1
    5364079     1
               ..
    5855927     1
    2255542     1
    2012532     1
    2028164     1
    3424901     1
    1180295     1
    4034188     1
    5983607     1
    3833367     1
    3665098     1
    342711      1
    2163355     1
    496285      1
    3515040     1
    831137      1
    1521315     1
    1798821     1
    3424934     1
    6096551     1
    57000       1
    2121385     1
    2735787     1
    5354943     1
    2137773     1
    2038446     1
    2455216     1
    2194098     1
    3051187     1
    2166453     1
    1106677     1
    Name: id, Length: 510, dtype: int64




```python
# check which countries did not find ids
no_id = merged_df[merged_df['id'] == 0]
no_id.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>city</th>
      <th>country</th>
      <th>coord</th>
      <th>id</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>7</th>
      <td>rosario</td>
      <td>br</td>
      <td></td>
      <td>0</td>
    </tr>
    <tr>
      <th>11</th>
      <td>khani</td>
      <td>ru</td>
      <td></td>
      <td>0</td>
    </tr>
    <tr>
      <th>12</th>
      <td>nikolskoye</td>
      <td>ru</td>
      <td></td>
      <td>0</td>
    </tr>
    <tr>
      <th>23</th>
      <td>taolanaro</td>
      <td>mg</td>
      <td></td>
      <td>0</td>
    </tr>
    <tr>
      <th>25</th>
      <td>mataura</td>
      <td>pf</td>
      <td></td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>




```python
#check how many without ids
len(no_id)
```




    94




```python
#trying to find lat and lng for cities missing ids from google geocoding api
g_url = 'https://maps.googleapis.com/maps/api/geocode/json?address='

counter = 0 #for check of all cities
for index,row in merged_df.iterrows():
    if row['id'] == 0:
        city = row['city']
        country = row['country']
        print('Now retrieving coordinates for city #%s: %s, %s' %(index, city, country))
        target_url = '%s%s,+%s&key=%s' % (g_url, city, country, gkey)
        print(target_url)
        try:
            response = req.get(target_url).json()
            response_path = response['results'][0]['geometry']['location']
            merged_df.set_value(index, 'coord', {'lon': response_path['lng'], 'lat': response_path['lat']})
        except:
            print('Missing Data for city #%s: %s,%s' %(index, city, country))
        counter += 1
#     if counter == 10:
#             break

print(counter) #to check for same number of records as no_id
```

    Now retrieving coordinates for city #7: rosario, br
    https://maps.googleapis.com/maps/api/geocode/json?address=rosario,+br&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #11: khani, ru
    https://maps.googleapis.com/maps/api/geocode/json?address=khani,+ru&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #12: nikolskoye, ru
    https://maps.googleapis.com/maps/api/geocode/json?address=nikolskoye,+ru&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #23: taolanaro, mg
    https://maps.googleapis.com/maps/api/geocode/json?address=taolanaro,+mg&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #25: mataura, pf
    https://maps.googleapis.com/maps/api/geocode/json?address=mataura,+pf&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #65: akyab, mm
    https://maps.googleapis.com/maps/api/geocode/json?address=akyab,+mm&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #68: bambey, sn
    https://maps.googleapis.com/maps/api/geocode/json?address=bambey,+sn&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #80: el balyana, eg
    https://maps.googleapis.com/maps/api/geocode/json?address=el balyana,+eg&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #82: palabuhanratu, id
    https://maps.googleapis.com/maps/api/geocode/json?address=palabuhanratu,+id&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #83: illoqqortoormiut, gl
    https://maps.googleapis.com/maps/api/geocode/json?address=illoqqortoormiut,+gl&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #84: puerto cortes, hn
    https://maps.googleapis.com/maps/api/geocode/json?address=puerto cortes,+hn&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #107: kerki, tm
    https://maps.googleapis.com/maps/api/geocode/json?address=kerki,+tm&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #113: raudeberg, no
    https://maps.googleapis.com/maps/api/geocode/json?address=raudeberg,+no&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #114: crab hill, bb
    https://maps.googleapis.com/maps/api/geocode/json?address=crab hill,+bb&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #119: kyzyl-suu, kg
    https://maps.googleapis.com/maps/api/geocode/json?address=kyzyl-suu,+kg&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #123: nizhneyansk, ru
    https://maps.googleapis.com/maps/api/geocode/json?address=nizhneyansk,+ru&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #136: tiruvottiyur, in
    https://maps.googleapis.com/maps/api/geocode/json?address=tiruvottiyur,+in&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #139: sohag, eg
    https://maps.googleapis.com/maps/api/geocode/json?address=sohag,+eg&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #144: kamogawa, jp
    https://maps.googleapis.com/maps/api/geocode/json?address=kamogawa,+jp&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #148: kerteh, my
    https://maps.googleapis.com/maps/api/geocode/json?address=kerteh,+my&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #154: temaraia, ki
    https://maps.googleapis.com/maps/api/geocode/json?address=temaraia,+ki&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Missing Data for city #154: temaraia,ki
    Now retrieving coordinates for city #163: sakakah, sa
    https://maps.googleapis.com/maps/api/geocode/json?address=sakakah,+sa&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #170: kaitangata, nz
    https://maps.googleapis.com/maps/api/geocode/json?address=kaitangata,+nz&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #176: umzimvubu, za
    https://maps.googleapis.com/maps/api/geocode/json?address=umzimvubu,+za&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #181: asau, tv
    https://maps.googleapis.com/maps/api/geocode/json?address=asau,+tv&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #194: santa eulalia del rio, es
    https://maps.googleapis.com/maps/api/geocode/json?address=santa eulalia del rio,+es&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #195: attawapiskat, ca
    https://maps.googleapis.com/maps/api/geocode/json?address=attawapiskat,+ca&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #199: samusu, ws
    https://maps.googleapis.com/maps/api/geocode/json?address=samusu,+ws&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #208: reefton, nz
    https://maps.googleapis.com/maps/api/geocode/json?address=reefton,+nz&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #214: barentsburg, sj
    https://maps.googleapis.com/maps/api/geocode/json?address=barentsburg,+sj&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #237: dzhusaly, kz
    https://maps.googleapis.com/maps/api/geocode/json?address=dzhusaly,+kz&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #243: codrington, ag
    https://maps.googleapis.com/maps/api/geocode/json?address=codrington,+ag&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #248: bayir, jo
    https://maps.googleapis.com/maps/api/geocode/json?address=bayir,+jo&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #253: sentyabrskiy, ru
    https://maps.googleapis.com/maps/api/geocode/json?address=sentyabrskiy,+ru&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #259: mys shmidta, ru
    https://maps.googleapis.com/maps/api/geocode/json?address=mys shmidta,+ru&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #263: avera, pf
    https://maps.googleapis.com/maps/api/geocode/json?address=avera,+pf&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #271: mikhaylovka, kz
    https://maps.googleapis.com/maps/api/geocode/json?address=mikhaylovka,+kz&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #276: japura, br
    https://maps.googleapis.com/maps/api/geocode/json?address=japura,+br&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #281: belushya guba, ru
    https://maps.googleapis.com/maps/api/geocode/json?address=belushya guba,+ru&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #282: jalu, ly
    https://maps.googleapis.com/maps/api/geocode/json?address=jalu,+ly&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #287: ruatoria, nz
    https://maps.googleapis.com/maps/api/geocode/json?address=ruatoria,+nz&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #300: airai, pw
    https://maps.googleapis.com/maps/api/geocode/json?address=airai,+pw&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #301: ambodifototra, mg
    https://maps.googleapis.com/maps/api/geocode/json?address=ambodifototra,+mg&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #303: saint anthony, ca
    https://maps.googleapis.com/maps/api/geocode/json?address=saint anthony,+ca&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #305: saint-georges, gf
    https://maps.googleapis.com/maps/api/geocode/json?address=saint-georges,+gf&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #307: amderma, ru
    https://maps.googleapis.com/maps/api/geocode/json?address=amderma,+ru&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #315: tumannyy, ru
    https://maps.googleapis.com/maps/api/geocode/json?address=tumannyy,+ru&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #317: formoso do araguaia, br
    https://maps.googleapis.com/maps/api/geocode/json?address=formoso do araguaia,+br&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #322: luang prabang, la
    https://maps.googleapis.com/maps/api/geocode/json?address=luang prabang,+la&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #344: solovetskiy, ru
    https://maps.googleapis.com/maps/api/geocode/json?address=solovetskiy,+ru&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #345: jiangyin, cn
    https://maps.googleapis.com/maps/api/geocode/json?address=jiangyin,+cn&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #350: grand river south east, mu
    https://maps.googleapis.com/maps/api/geocode/json?address=grand river south east,+mu&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #351: tabiauea, ki
    https://maps.googleapis.com/maps/api/geocode/json?address=tabiauea,+ki&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #356: vaitupu, wf
    https://maps.googleapis.com/maps/api/geocode/json?address=vaitupu,+wf&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #377: lasa, cn
    https://maps.googleapis.com/maps/api/geocode/json?address=lasa,+cn&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #385: doctor pedro p. pena, py
    https://maps.googleapis.com/maps/api/geocode/json?address=doctor pedro p. pena,+py&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #386: marcona, pe
    https://maps.googleapis.com/maps/api/geocode/json?address=marcona,+pe&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #450: gorno-chuyskiy, ru
    https://maps.googleapis.com/maps/api/geocode/json?address=gorno-chuyskiy,+ru&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #466: tarudant, ma
    https://maps.googleapis.com/maps/api/geocode/json?address=tarudant,+ma&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #467: odweyne, so
    https://maps.googleapis.com/maps/api/geocode/json?address=odweyne,+so&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #475: talawdi, sd
    https://maps.googleapis.com/maps/api/geocode/json?address=talawdi,+sd&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #482: tsihombe, mg
    https://maps.googleapis.com/maps/api/geocode/json?address=tsihombe,+mg&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #483: phan rang, vn
    https://maps.googleapis.com/maps/api/geocode/json?address=phan rang,+vn&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #494: privokzalnyy, ru
    https://maps.googleapis.com/maps/api/geocode/json?address=privokzalnyy,+ru&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #497: biak, id
    https://maps.googleapis.com/maps/api/geocode/json?address=biak,+id&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #523: wulanhaote, cn
    https://maps.googleapis.com/maps/api/geocode/json?address=wulanhaote,+cn&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Missing Data for city #523: wulanhaote,cn
    Now retrieving coordinates for city #537: bolungarvik, is
    https://maps.googleapis.com/maps/api/geocode/json?address=bolungarvik,+is&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #579: saleaula, ws
    https://maps.googleapis.com/maps/api/geocode/json?address=saleaula,+ws&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #580: rincon, an
    https://maps.googleapis.com/maps/api/geocode/json?address=rincon,+an&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #581: canitas, mx
    https://maps.googleapis.com/maps/api/geocode/json?address=canitas,+mx&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #586: bud, no
    https://maps.googleapis.com/maps/api/geocode/json?address=bud,+no&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #593: kadykchan, ru
    https://maps.googleapis.com/maps/api/geocode/json?address=kadykchan,+ru&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #603: itarema, br
    https://maps.googleapis.com/maps/api/geocode/json?address=itarema,+br&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #605: bobo dioulasso, bf
    https://maps.googleapis.com/maps/api/geocode/json?address=bobo dioulasso,+bf&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #611: lolua, tv
    https://maps.googleapis.com/maps/api/geocode/json?address=lolua,+tv&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Missing Data for city #611: lolua,tv
    Now retrieving coordinates for city #633: warqla, dz
    https://maps.googleapis.com/maps/api/geocode/json?address=warqla,+dz&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Missing Data for city #633: warqla,dz
    Now retrieving coordinates for city #643: lar, ir
    https://maps.googleapis.com/maps/api/geocode/json?address=lar,+ir&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #648: tkibuli, ge
    https://maps.googleapis.com/maps/api/geocode/json?address=tkibuli,+ge&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #652: stoyba, ru
    https://maps.googleapis.com/maps/api/geocode/json?address=stoyba,+ru&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #655: henties bay, na
    https://maps.googleapis.com/maps/api/geocode/json?address=henties bay,+na&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #660: garowe, so
    https://maps.googleapis.com/maps/api/geocode/json?address=garowe,+so&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #670: bairiki, ki
    https://maps.googleapis.com/maps/api/geocode/json?address=bairiki,+ki&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #673: qena, eg
    https://maps.googleapis.com/maps/api/geocode/json?address=qena,+eg&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #676: doha, kw
    https://maps.googleapis.com/maps/api/geocode/json?address=doha,+kw&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #686: buin, pg
    https://maps.googleapis.com/maps/api/geocode/json?address=buin,+pg&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #688: lethem, gy
    https://maps.googleapis.com/maps/api/geocode/json?address=lethem,+gy&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #689: karaul, ru
    https://maps.googleapis.com/maps/api/geocode/json?address=karaul,+ru&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #691: andevoranto, mg
    https://maps.googleapis.com/maps/api/geocode/json?address=andevoranto,+mg&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #694: bacuit, ph
    https://maps.googleapis.com/maps/api/geocode/json?address=bacuit,+ph&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #707: halalo, wf
    https://maps.googleapis.com/maps/api/geocode/json?address=halalo,+wf&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #713: ajtos, bg
    https://maps.googleapis.com/maps/api/geocode/json?address=ajtos,+bg&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #727: tungkang, tw
    https://maps.googleapis.com/maps/api/geocode/json?address=tungkang,+tw&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #728: las palmas, es
    https://maps.googleapis.com/maps/api/geocode/json?address=las palmas,+es&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    Now retrieving coordinates for city #743: naral, bd
    https://maps.googleapis.com/maps/api/geocode/json?address=naral,+bd&key=AIzaSyCjJqwo5ZEpTnFQo4MwagogurWbUnpOd2U
    94
    


```python
#preview merged_df
merged_df.head(30)
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>city</th>
      <th>country</th>
      <th>coord</th>
      <th>id</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>adrar</td>
      <td>dz</td>
      <td>{'lon': -0.29388000000000003, 'lat': 27.87429}</td>
      <td>2508813</td>
    </tr>
    <tr>
      <th>1</th>
      <td>barrow</td>
      <td>us</td>
      <td>{'lon': -156.788727, 'lat': 71.290581}</td>
      <td>5880054</td>
    </tr>
    <tr>
      <th>2</th>
      <td>palmer</td>
      <td>us</td>
      <td>{'lon': -98.257294, 'lat': 41.22224}</td>
      <td>5074769</td>
    </tr>
    <tr>
      <th>6</th>
      <td>punta arenas</td>
      <td>cl</td>
      <td>{'lon': -70.916672, 'lat': -53.150002}</td>
      <td>3874787</td>
    </tr>
    <tr>
      <th>7</th>
      <td>rosario</td>
      <td>br</td>
      <td>{'lon': -44.2493388, 'lat': -2.9410215}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>8</th>
      <td>puerto leguizamo</td>
      <td>co</td>
      <td>{'lon': -74.781891, 'lat': -0.19337000000000001}</td>
      <td>3671437</td>
    </tr>
    <tr>
      <th>9</th>
      <td>tasiilaq</td>
      <td>gl</td>
      <td>{'lon': -37.636761, 'lat': 65.61451}</td>
      <td>3424607</td>
    </tr>
    <tr>
      <th>10</th>
      <td>salekhard</td>
      <td>ru</td>
      <td>{'lon': 66.601936, 'lat': 66.529999}</td>
      <td>1493197</td>
    </tr>
    <tr>
      <th>11</th>
      <td>khani</td>
      <td>ru</td>
      <td>{'lon': 119.965, 'lat': 56.933333}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>12</th>
      <td>nikolskoye</td>
      <td>ru</td>
      <td>{'lon': 166.0015368, 'lat': 55.1981604}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>13</th>
      <td>narsaq</td>
      <td>gl</td>
      <td>{'lon': -46.049999, 'lat': 60.916672}</td>
      <td>3421719</td>
    </tr>
    <tr>
      <th>14</th>
      <td>busselton</td>
      <td>au</td>
      <td>{'lon': 115.370796, 'lat': -33.684769}</td>
      <td>7839477</td>
    </tr>
    <tr>
      <th>16</th>
      <td>faanui</td>
      <td>pf</td>
      <td>{'lon': -151.75, 'lat': -16.48333}</td>
      <td>4034551</td>
    </tr>
    <tr>
      <th>17</th>
      <td>kapaa</td>
      <td>us</td>
      <td>{'lon': -159.318954, 'lat': 22.075211}</td>
      <td>5848280</td>
    </tr>
    <tr>
      <th>18</th>
      <td>port elizabeth</td>
      <td>za</td>
      <td>{'lon': 25.57007, 'lat': -33.917992}</td>
      <td>964420</td>
    </tr>
    <tr>
      <th>19</th>
      <td>pevek</td>
      <td>ru</td>
      <td>{'lon': 170.313324, 'lat': 69.700829}</td>
      <td>2122090</td>
    </tr>
    <tr>
      <th>20</th>
      <td>ponta do sol</td>
      <td>cv</td>
      <td>{'lon': -25.091921, 'lat': 17.199421}</td>
      <td>3374346</td>
    </tr>
    <tr>
      <th>21</th>
      <td>rikitea</td>
      <td>pf</td>
      <td>{'lon': -134.969177, 'lat': -23.120279}</td>
      <td>4030556</td>
    </tr>
    <tr>
      <th>22</th>
      <td>tautira</td>
      <td>pf</td>
      <td>{'lon': -149.149994, 'lat': -17.73333}</td>
      <td>4033557</td>
    </tr>
    <tr>
      <th>23</th>
      <td>taolanaro</td>
      <td>mg</td>
      <td>{'lon': 46.9853688, 'lat': -25.0225309}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>24</th>
      <td>berlevag</td>
      <td>no</td>
      <td>{'lon': 29.086361, 'lat': 70.85778}</td>
      <td>780687</td>
    </tr>
    <tr>
      <th>25</th>
      <td>mataura</td>
      <td>pf</td>
      <td>{'lon': -149.4850445, 'lat': -23.3470634}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>26</th>
      <td>tiarei</td>
      <td>pf</td>
      <td>{'lon': -149.333328, 'lat': -17.533331}</td>
      <td>4033356</td>
    </tr>
    <tr>
      <th>27</th>
      <td>havoysund</td>
      <td>no</td>
      <td>{'lon': 24.66217, 'lat': 70.996338}</td>
      <td>779622</td>
    </tr>
    <tr>
      <th>28</th>
      <td>yumen</td>
      <td>cn</td>
      <td>{'lon': 97.199997, 'lat': 40.283329}</td>
      <td>1528998</td>
    </tr>
    <tr>
      <th>29</th>
      <td>hithadhoo</td>
      <td>mv</td>
      <td>{'lon': 73.083328, 'lat': -0.6000000000000001}</td>
      <td>1282256</td>
    </tr>
    <tr>
      <th>30</th>
      <td>ushuaia</td>
      <td>ar</td>
      <td>{'lon': -68.300003, 'lat': -54.799999}</td>
      <td>3833367</td>
    </tr>
    <tr>
      <th>31</th>
      <td>hammerfest</td>
      <td>no</td>
      <td>{'lon': 23.682091, 'lat': 70.663361}</td>
      <td>779683</td>
    </tr>
    <tr>
      <th>33</th>
      <td>sao filipe</td>
      <td>cv</td>
      <td>{'lon': -24.49556, 'lat': 14.8961}</td>
      <td>3374210</td>
    </tr>
    <tr>
      <th>34</th>
      <td>batemans bay</td>
      <td>au</td>
      <td>{'lon': 150.183334, 'lat': -35.716671}</td>
      <td>2176639</td>
    </tr>
  </tbody>
</table>
</div>




```python
#check with below
len(merged_df)
```




    603




```python
#check with above
rec_check
```




    603




```python
#check to see how many records with no coordinates
no_coord = merged_df[merged_df['coord'] == ""]
no_coord
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>city</th>
      <th>country</th>
      <th>coord</th>
      <th>id</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>154</th>
      <td>temaraia</td>
      <td>ki</td>
      <td></td>
      <td>0</td>
    </tr>
    <tr>
      <th>523</th>
      <td>wulanhaote</td>
      <td>cn</td>
      <td></td>
      <td>0</td>
    </tr>
    <tr>
      <th>611</th>
      <td>lolua</td>
      <td>tv</td>
      <td></td>
      <td>0</td>
    </tr>
    <tr>
      <th>633</th>
      <td>warqla</td>
      <td>dz</td>
      <td></td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>




```python
# of records without coordinates
len(no_coord)
```




    4




```python
#leave merged_df the same from here on
weather_data = merged_df.copy()
```


```python
#preview weather_data to check for success
weather_data.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>city</th>
      <th>country</th>
      <th>coord</th>
      <th>id</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>adrar</td>
      <td>dz</td>
      <td>{'lon': -0.29388000000000003, 'lat': 27.87429}</td>
      <td>2508813</td>
    </tr>
    <tr>
      <th>1</th>
      <td>barrow</td>
      <td>us</td>
      <td>{'lon': -156.788727, 'lat': 71.290581}</td>
      <td>5880054</td>
    </tr>
    <tr>
      <th>2</th>
      <td>palmer</td>
      <td>us</td>
      <td>{'lon': -98.257294, 'lat': 41.22224}</td>
      <td>5074769</td>
    </tr>
    <tr>
      <th>6</th>
      <td>punta arenas</td>
      <td>cl</td>
      <td>{'lon': -70.916672, 'lat': -53.150002}</td>
      <td>3874787</td>
    </tr>
    <tr>
      <th>7</th>
      <td>rosario</td>
      <td>br</td>
      <td>{'lon': -44.2493388, 'lat': -2.9410215}</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Open Weather Maps Api example links for reference
# id url example: 'api.openweathermap.org/data/2.5/weather?id=2172797'
# coord url example: 'api.openweathermap.org/data/2.5/weather?lat=35&lon=139'
# city search use : api.openweathermap.org/data/2.5/weather?q=London,uk
# remember to use &appid= for key

counter = 0 #for breaking and pausing
cur_err_list = [] # for cities without data from current weather
for_err_list = [] # for cities without data from forecast data
cur_errors = 0  #current weather pull errors
for_errors = 0 #forecast weather pull errors

#create additional columns for open weather map data

#make columnds for lat and lng from open weather source
weather_data['lat'] = ""
weather_data['lng'] = ""

#make columns for current weather data (at time of pull)
weather_data['cur_date'] = ""
weather_data['cur_temp'] = ""
weather_data['cur_humidity'] = ""
weather_data['cur_clouds'] = ""
weather_data['cur_wind'] = ""

# make columns for records corresponding to the highest temperature 
# forecasted in the next 24 hours (from time of pull)
weather_data['max_date'] = ""
weather_data['max_temp'] = ""
weather_data['max_temp_humidity'] = ""
weather_data['max_temp_clouds'] = ""
weather_data['max_temp_wind'] = ""

# make columns for records corresponding to the average values
# forecasted in the next 5 days (from time of pull)
weather_data['avg_date0'] = ""
weather_data['avg_date1'] = ""
weather_data['avg_temp'] = ""
weather_data['avg_humidity'] = ""
weather_data['avg_clouds'] = ""
weather_data['avg_wind'] = ""

t0 = time.time() #for pause timer
for index, row in weather_data.iterrows():
    print('Now retrieving data for city #%s: %s, %s' % (index, row['city'], row['country']))
    #uses url believed to be most accurate
    if ((row['id']) == 0) and (row['coord'] != ""): # coordinates if no id, but with coordinates
        lat = row['coord']['lat']
        lon = row['coord']['lon']
        cur_url = 'https://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&APPID=%s&units=imperial' % (lat, lon, wkey)  
        for_url = 'https://api.openweathermap.org/data/2.5/forecast?lat=%s&lon=%s&APPID=%s&units=imperial' % (lat, lon, wkey)  
    elif row['id'] != 0: # use if if ID exists
        loc_id = row['id']
        cur_url = 'https://api.openweathermap.org/data/2.5/weather?id=%s&APPID=%s&units=imperial' % (loc_id, wkey)
        for_url = 'https://api.openweathermap.org/data/2.5/forecast?id=%s&APPID=%s&units=imperial' % (loc_id, wkey)
    else: #use city and country if no id AND no coordinates
        city = row['city']
        country = row['country']
        cur_url = 'https://api.openweathermap.org/data/2.5/weather?q=%s,%s&APPID=%s&units=imperial' % (city, country, wkey)
        for_url = 'https://api.openweathermap.org/data/2.5/forecast?q=%s,%s&APPID=%s&units=imperial' % (city, country, wkey)
    print('Current Weather URL:')
    print(cur_url)
    print('Forecast Weather URL:')
    print(for_url)
    #get current weather data
    try:
        cur_response = req.get(cur_url).json()
        weather_data.set_value(index, 'lat', cur_response['coord']['lat'])
        weather_data.set_value(index, 'lng', cur_response['coord']['lon'])
        weather_data.set_value(index, 'cur_date', cur_response['dt'])
        weather_data.set_value(index, 'cur_temp', cur_response['main']['temp'])
        weather_data.set_value(index, 'cur_humidity', cur_response['main']['humidity'])
        weather_data.set_value(index, 'cur_clouds', cur_response['clouds']['all'])
        weather_data.set_value(index, 'cur_wind', cur_response['wind']['speed'])
    except:
        print('Missing Current Weather Info for city #%s: %s, %s' % (index, row['city'], row['country']))
        cur_err_list.append(index)
        cur_errors += 1
    try:
        #get max temperature weather data
        for_response = req.get(for_url).json()
        for_path = for_response['list']
        temps_24h = [] # a list of temp over a 24 hours period forecased every 3 hours
        for n in range(9): # a 24 hour period
            temps_24h.append(for_path[n]['main']['temp_max'])
        max_index = temps_24h.index(max(temps_24h))
        weather_data.set_value(index, 'max_date', for_path[max_index]['dt'])
        weather_data.set_value(index, 'max_temp', for_path[max_index]['main']['temp_max'])
        weather_data.set_value(index, 'max_temp_humidity', for_path[max_index]['main']['humidity'])
        weather_data.set_value(index, 'max_temp_clouds', for_path[max_index]['clouds']['all'])
        weather_data.set_value(index, 'max_temp_wind', for_path[max_index]['wind']['speed'])
        # get avg forecast values 
        #set up blank lists for dates, temperature, clouds, wind, humidity over a 5 day period
        dat = []
        tem = []
        clo = []
        win = []
        hum = []
        for n in for_path: # 5 days worth of forecast
            dat.append(n['dt'])
            tem.append(n['main']['temp'])
            clo.append(n['clouds']['all'])
            win.append(n['wind']['speed'])
            hum.append(n['main']['humidity'])
        weather_data.set_value(index, 'avg_date0', dat[0]) #beginning date
        weather_data.set_value(index, 'avg_date1', dat[-1]) #ending date
        weather_data.set_value(index, 'avg_temp', np.mean(tem)) # mean temp over 5 days
        weather_data.set_value(index, 'avg_humidity', np.mean(hum)) #mean humidity over 5 days
        weather_data.set_value(index, 'avg_clouds', np.mean(clo)) #mean cloud cover over 5 days
        weather_data.set_value(index, 'avg_wind', np.mean(win)) #mean wind speed over 5 days
    except:
        print('Missing Forecast Info for city #%s: %s, %s' % (index, row['city'], row['country']))
        for_err_list.append(index)
        for_errors += 1
    print('---------------------------------------------------------------------------')
    counter +=1
    if counter % 30 == 0: #because two records pulled for each city 
        t1 = time.time() #records time very 30 records
        sl_time = 70 - (t1-t0) # calculates buffer for api pull limit
        print("")
        print('********Sleeping for %s seconds.********' % (sl_time))
        print("")
        time.sleep(sl_time) # pauses for appropraite amount of time
        t0 = time.time() # resets for next 30 pull timer
#     if counter == 5:
#         break

```

    Now retrieving data for city #0: adrar, dz
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2508813&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2508813&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #1: barrow, us
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=5880054&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=5880054&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #2: palmer, us
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=5074769&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=5074769&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #6: punta arenas, cl
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3874787&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3874787&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #7: rosario, br
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=-2.9410215&lon=-44.2493388&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=-2.9410215&lon=-44.2493388&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #8: puerto leguizamo, co
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3671437&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3671437&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #9: tasiilaq, gl
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3424607&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3424607&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #10: salekhard, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1493197&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1493197&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #11: khani, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=56.933333&lon=119.965&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=56.933333&lon=119.965&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #12: nikolskoye, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=55.1981604&lon=166.0015368&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=55.1981604&lon=166.0015368&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #13: narsaq, gl
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3421719&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3421719&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #14: busselton, au
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=7839477&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=7839477&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #16: faanui, pf
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=4034551&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=4034551&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #17: kapaa, us
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=5848280&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=5848280&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #18: port elizabeth, za
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=964420&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=964420&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #19: pevek, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2122090&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2122090&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #20: ponta do sol, cv
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3374346&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3374346&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #21: rikitea, pf
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=4030556&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=4030556&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #22: tautira, pf
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=4033557&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=4033557&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #23: taolanaro, mg
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=-25.0225309&lon=46.9853688&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=-25.0225309&lon=46.9853688&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #24: berlevag, no
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=780687&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=780687&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #25: mataura, pf
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=-23.3470634&lon=-149.4850445&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=-23.3470634&lon=-149.4850445&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #26: tiarei, pf
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=4033356&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=4033356&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #27: havoysund, no
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=779622&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=779622&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #28: yumen, cn
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1528998&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1528998&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #29: hithadhoo, mv
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1282256&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1282256&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #30: ushuaia, ar
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3833367&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3833367&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #31: hammerfest, no
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=779683&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=779683&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #33: sao filipe, cv
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3374210&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3374210&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #34: batemans bay, au
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2176639&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2176639&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    
    ********Sleeping for 50.17125630378723 seconds.********
    
    Now retrieving data for city #35: kita, ml
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2455216&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2455216&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #36: ilulissat, gl
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3423146&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3423146&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #37: vostok, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2013279&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2013279&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #39: ambunti, pg
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2100933&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2100933&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #40: hermanus, za
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3366880&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3366880&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #41: bluff, nz
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2206939&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2206939&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #42: meulaboh, id
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1214488&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1214488&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #43: banda aceh, id
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1215501&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1215501&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #45: raghogarh, in
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1259056&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1259056&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #46: masunga, bw
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=933390&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=933390&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #47: qaanaaq, gl
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3831208&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3831208&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #48: russkiy kameshkir, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=500400&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=500400&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #49: saint george, bm
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3573062&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3573062&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #51: chokurdakh, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2126123&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2126123&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #52: bambous virieux, mu
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1106677&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1106677&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #53: hobart, au
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2163355&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2163355&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #55: coihaique, cl
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3894426&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3894426&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #56: tuktoyaktuk, ca
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=6170031&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=6170031&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #57: severo-kurilsk, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2121385&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2121385&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #58: ancud, cl
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3899695&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3899695&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #59: victoria, sc
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=241131&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=241131&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #60: fortuna, us
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=5563839&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=5563839&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #61: tuatapere, nz
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2180815&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2180815&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #62: vila velha, br
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3445026&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3445026&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #63: san patricio, mx
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3985168&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3985168&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #64: yulara, au
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=6355222&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=6355222&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #65: akyab, mm
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=20.1527657&lon=92.86768610000001&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=20.1527657&lon=92.86768610000001&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #66: kangaatsiaq, gl
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3422683&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3422683&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #67: cape town, za
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3369157&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3369157&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #68: bambey, sn
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=14.6965115&lon=-16.458256&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=14.6965115&lon=-16.458256&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    
    ********Sleeping for 50.54035258293152 seconds.********
    
    Now retrieving data for city #69: laredo, es
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=6360682&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=6360682&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #71: albany, au
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=7839657&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=7839657&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #73: port alfred, za
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=964432&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=964432&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #74: guerrero negro, mx
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=4021858&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=4021858&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #75: jamestown, sh
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3370903&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3370903&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #76: tepic, mx
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3981941&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3981941&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #77: provideniya, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=4031574&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=4031574&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #78: sumenep, id
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1626099&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1626099&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #79: mahebourg, mu
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=934322&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=934322&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #80: el balyana, eg
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=26.2354377&lon=32.0029805&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=26.2354377&lon=32.0029805&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #81: khandyga, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2022773&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2022773&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #82: palabuhanratu, id
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=-6.9852341&lon=106.5475399&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=-6.9852341&lon=106.5475399&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #83: illoqqortoormiut, gl
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=70.48556909999999&lon=-21.9628757&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=70.48556909999999&lon=-21.9628757&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #84: puerto cortes, hn
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=15.825072&lon=-87.92857769999999&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=15.825072&lon=-87.92857769999999&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #85: dhidhdhoo, mv
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1337612&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1337612&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #86: namibe, ao
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3347019&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3347019&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #87: bredasdorp, za
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1015776&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1015776&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #88: rocha, uy
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3440777&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3440777&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #89: bethel, us
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=4182260&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=4182260&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #100: puerto escondido, mx
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3520994&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3520994&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #101: chuy, uy
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3443061&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3443061&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #102: port hedland, au
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=7839630&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=7839630&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #104: the valley, ai
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3573374&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3573374&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #105: aasiaat, gl
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3424901&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3424901&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #106: suleja, ng
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2322794&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2322794&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #107: kerki, tm
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=37.8099917&lon=65.2026017&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=37.8099917&lon=65.2026017&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #108: lavrentiya, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=4031637&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=4031637&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #109: atuona, pf
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=4020109&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=4020109&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #110: kalmunai, lk
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1242110&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1242110&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #111: tazovskiy, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1489853&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1489853&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    
    ********Sleeping for 51.07042074203491 seconds.********
    
    Now retrieving data for city #112: avarua, ck
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=4035715&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=4035715&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #113: raudeberg, no
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=61.9829132&lon=5.1351057&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=61.9829132&lon=5.1351057&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #114: crab hill, bb
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=13.3216196&lon=-59.63555170000001&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=13.3216196&lon=-59.63555170000001&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #115: touros, br
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3386213&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3386213&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #116: yellowknife, ca
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=6185377&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=6185377&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #117: longyearbyen, sj
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2729907&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2729907&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #118: tessalit, ml
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2449893&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2449893&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #119: kyzyl-suu, kg
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=42.3430331&lon=78.0052678&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=42.3430331&lon=78.0052678&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #120: bardiyah, ly
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=80509&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=80509&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #121: new norfolk, au
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2155415&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2155415&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #122: fairbanks, us
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=5861897&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=5861897&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #123: nizhneyansk, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=71.450058&lon=136.1122279&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=71.450058&lon=136.1122279&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #124: vaini, to
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=4032243&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=4032243&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #125: troitskoye, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=481501&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=481501&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #135: east london, za
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1006984&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1006984&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #136: tiruvottiyur, in
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=13.1691914&lon=80.3045793&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=13.1691914&lon=80.3045793&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #137: kodiak, us
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=5866583&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=5866583&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #138: doha, qa
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=290030&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=290030&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #139: sohag, eg
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=26.5590737&lon=31.6956705&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=26.5590737&lon=31.6956705&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #140: geraldton, au
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2070998&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2070998&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #141: ondjiva, ao
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3346821&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3346821&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #142: dikson, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1507390&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1507390&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #143: santa maria, py
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3436977&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3436977&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #144: kamogawa, jp
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=35.1139867&lon=140.0987111&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=35.1139867&lon=140.0987111&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #145: nanhai, cn
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=7696234&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=7696234&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #146: ravar, ir
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=118704&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=118704&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #147: boguchany, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1509844&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1509844&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #148: kerteh, my
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=4.507893999999999&lon=103.4430001&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=4.507893999999999&lon=103.4430001&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #149: katsuura, jp
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2112309&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2112309&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #150: boyuibe, bo
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3923015&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3923015&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    
    ********Sleeping for 34.84830951690674 seconds.********
    
    Now retrieving data for city #151: eskisehir, tr
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=315202&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=315202&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #152: zboriv, ua
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=687449&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=687449&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #153: baykit, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1510689&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1510689&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #154: temaraia, ki
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?q=temaraia,ki&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?q=temaraia,ki&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Missing Current Weather Info for city #154: temaraia, ki
    Missing Forecast Info for city #154: temaraia, ki
    ---------------------------------------------------------------------------
    Now retrieving data for city #155: marawi, sd
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=370481&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=370481&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #156: nouadhibou, mr
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2377457&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2377457&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #157: sitka, us
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=5557293&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=5557293&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #158: ahipara, nz
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2194098&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2194098&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #159: pangody, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1495626&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1495626&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #160: kousseri, cm
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2229798&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2229798&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #161: thinadhoo, mv
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1337610&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1337610&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #162: shache, cn
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1280037&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1280037&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #163: sakakah, sa
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=29.87800309999999&lon=40.1043057&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=29.87800309999999&lon=40.1043057&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #164: pouebo, nc
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2138607&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2138607&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #165: butaritari, ki
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=7521588&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=7521588&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #167: ballina, au
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=7839686&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=7839686&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #169: pacific grove, us
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=5380437&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=5380437&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #170: kaitangata, nz
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=-46.28334&lon=169.8470967&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=-46.28334&lon=169.8470967&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #171: hilo, us
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=5855927&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=5855927&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #172: yenagoa, ng
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2318123&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2318123&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #173: saint-philippe, re
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=6690301&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=6690301&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #175: san quintin, mx
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3984997&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3984997&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #176: umzimvubu, za
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=-30.7781755&lon=28.9528645&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=-30.7781755&lon=28.9528645&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #177: gold coast, au
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=7839581&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=7839581&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #179: dunedin, nz
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2191562&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2191562&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #180: leningradskiy, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2123814&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2123814&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #181: asau, tv
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=-7.488197&lon=178.6807179&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=-7.488197&lon=178.6807179&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #182: puerto ayora, ec
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3652764&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3652764&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #183: emerald, au
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2167425&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2167425&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #185: carnarvon, au
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2074865&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2074865&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    
    ********Sleeping for 50.71479344367981 seconds.********
    
    Now retrieving data for city #186: maragogi, br
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3395458&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3395458&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #187: upernavik, gl
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3418910&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3418910&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #188: hanna, ca
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=5970234&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=5970234&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #189: yelizovo, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2119538&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2119538&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #190: houma, us
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=4328010&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=4328010&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #191: ocos, gt
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3592086&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3592086&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #192: grand gaube, mu
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=934479&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=934479&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #193: cabo san lucas, mx
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3985710&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3985710&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #194: santa eulalia del rio, es
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=38.9852809&lon=1.5351065&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=38.9852809&lon=1.5351065&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #195: attawapiskat, ca
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=52.9258846&lon=-82.42889219999999&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=52.9258846&lon=-82.42889219999999&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #196: lorengau, pg
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2092164&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2092164&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #197: bandarbeyla, so
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=64814&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=64814&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #198: castro, cl
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3896218&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3896218&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #199: samusu, ws
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=-14.0056774&lon=-171.4299586&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=-14.0056774&lon=-171.4299586&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #200: coffs harbour, au
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2171085&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2171085&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #202: minab, ir
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=123941&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=123941&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #203: torbay, ca
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=6167817&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=6167817&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #204: beloha, mg
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1067565&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1067565&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #205: saint-francois, gp
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3578441&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3578441&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #206: praia da vitoria, pt
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3372760&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3372760&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #207: dekar, bw
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=933815&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=933815&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #208: reefton, nz
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=-42.1145664&lon=171.8625025&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=-42.1145664&lon=171.8625025&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #209: zhuhai, cn
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1790437&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1790437&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #210: cayenne, gf
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=6690689&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=6690689&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #212: kupang, id
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2057087&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2057087&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #213: dudinka, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1507116&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1507116&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #214: barentsburg, sj
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=78.0648475&lon=14.2334597&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=78.0648475&lon=14.2334597&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #215: khatanga, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2022572&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2022572&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #216: bloomfield, us
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=5095779&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=5095779&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #224: thompson, ca
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=6165406&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=6165406&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    
    ********Sleeping for 50.9599723815918 seconds.********
    
    Now retrieving data for city #225: dauphin, ca
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=5935341&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=5935341&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #226: bengkulu, id
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1649150&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1649150&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #227: bay roberts, ca
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=5895424&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=5895424&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #228: moerai, pf
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=4034188&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=4034188&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #229: hofn, is
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2630299&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2630299&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #230: ostrovnoy, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=556268&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=556268&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #231: ribeira grande, pt
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=8010689&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=8010689&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #233: peniche, pt
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=8010554&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=8010554&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #235: camacha, pt
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2270385&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2270385&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #237: dzhusaly, kz
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=50.6602258&lon=58.2691484&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=50.6602258&lon=58.2691484&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #238: ixtapa, mx
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=4004293&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=4004293&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #241: tulum, mx
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3515040&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3515040&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #242: salalah, om
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=286621&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=286621&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #243: codrington, ag
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=17.6425736&lon=-61.8204456&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=17.6425736&lon=-61.8204456&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #244: portland, au
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2152667&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2152667&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #246: cockburn town, bs
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3572627&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3572627&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #247: kavieng, pg
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2094342&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2094342&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #248: bayir, jo
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=30.7617321&lon=36.6793491&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=30.7617321&lon=36.6793491&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #249: san francisco, ar
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3837675&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3837675&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #250: oktyabrskiy, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=515879&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=515879&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #253: sentyabrskiy, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=60.493056&lon=72.19638909999999&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=60.493056&lon=72.19638909999999&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #254: great falls, us
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=5655240&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=5655240&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #257: cidreira, br
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3466165&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3466165&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #258: sioux lookout, ca
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=6148373&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=6148373&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #259: mys shmidta, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=68.884224&lon=-179.4311219&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=68.884224&lon=-179.4311219&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #260: san pedro, bz
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3581164&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3581164&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #261: kincardine, ca
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=5992144&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=5992144&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #262: vestmannaeyjar, is
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3412093&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3412093&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #263: avera, pf
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=43.4100689&lon=-94.83355019999999&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=43.4100689&lon=-94.83355019999999&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #264: port macquarie, au
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2152659&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2152659&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    
    ********Sleeping for 50.82317018508911 seconds.********
    
    Now retrieving data for city #265: aklavik, ca
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=5882953&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=5882953&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #266: talnakh, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1490256&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1490256&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #267: marfino, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=529368&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=529368&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #269: lebu, cl
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3883457&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3883457&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #270: sao joao da barra, br
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3448903&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3448903&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #271: mikhaylovka, kz
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=53.8263706&lon=76.55165459999999&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=53.8263706&lon=76.55165459999999&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #272: catalina, ca
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=5918243&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=5918243&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #273: iznoski, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=554776&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=554776&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #274: port lincoln, au
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=7839452&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=7839452&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #276: japura, br
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=-1.8827204&lon=-66.9295891&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=-1.8827204&lon=-66.9295891&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #277: bubaque, gw
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2374583&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2374583&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #278: hambantota, lk
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1244926&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1244926&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #279: warmbad, na
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3352263&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3352263&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #280: noumea, nc
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2139521&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2139521&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #281: belushya guba, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=71.54555599999999&lon=52.32027799999999&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=71.54555599999999&lon=52.32027799999999&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #282: jalu, ly
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=29.040621&lon=21.4991334&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=29.040621&lon=21.4991334&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #283: joshimath, in
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1268814&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1268814&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #284: cerritos, mx
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=4014795&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=4014795&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #285: vao, nc
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2137773&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2137773&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #286: chepareria, ke
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=199604&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=199604&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #287: ruatoria, nz
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=-37.8927614&lon=178.3194507&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=-37.8927614&lon=178.3194507&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #288: mezen, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=527321&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=527321&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #289: deputatskiy, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2028164&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2028164&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #290: bonthe, sl
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2409914&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2409914&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #291: rio grande, br
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3451138&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3451138&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #292: barcelos, br
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3665098&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3665098&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #293: asosa, et
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=343292&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=343292&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #294: chara, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2025630&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2025630&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #295: nome, us
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=5870133&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=5870133&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #296: quang ngai, vn
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1568770&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1568770&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    
    ********Sleeping for 50.89634895324707 seconds.********
    
    Now retrieving data for city #297: klaksvik, fo
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2618795&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2618795&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #298: namatanai, pg
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2090021&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2090021&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #299: husavik, is
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2629833&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2629833&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #300: airai, pw
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=7.396611799999999&lon=134.5690225&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=7.396611799999999&lon=134.5690225&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #301: ambodifototra, mg
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=-16.99824&lon=49.85258899999999&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=-16.99824&lon=49.85258899999999&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #302: esperance, au
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2071860&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2071860&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #303: saint anthony, ca
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=33.7746056&lon=-118.1819309&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=33.7746056&lon=-118.1819309&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #304: coruripe, br
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3465329&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3465329&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #305: saint-georges, gf
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=3.8925718&lon=-51.807382&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=3.8925718&lon=-51.807382&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #306: ponta do sol, pt
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2264557&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2264557&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #307: amderma, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=69.751221&lon=61.6636961&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=69.751221&lon=61.6636961&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #308: lucapa, ao
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=145724&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=145724&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #309: normal, us
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=4903780&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=4903780&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #310: najran, sa
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=103630&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=103630&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #311: borogontsy, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2026160&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2026160&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #312: kuusamo, fi
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=649925&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=649925&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #314: baoqing, cn
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2038446&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2038446&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #315: tumannyy, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=54.0873125&lon=90.3269882&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=54.0873125&lon=90.3269882&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #316: mildura, au
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2157698&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2157698&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #317: formoso do araguaia, br
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=-11.8031151&lon=-50.1832516&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=-11.8031151&lon=-50.1832516&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #318: channel-port aux basques, ca
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=5919815&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=5919815&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #319: ardon, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=581178&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=581178&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #321: atasu, kz
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1526041&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1526041&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #322: luang prabang, la
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=19.8833959&lon=102.1346874&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=19.8833959&lon=102.1346874&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #323: ayan, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2027317&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2027317&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #325: bangonay, ph
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1727237&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1727237&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #326: kruisfontein, za
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=986717&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=986717&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #327: aldan, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2027968&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2027968&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #328: santa marta, co
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3668605&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3668605&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #329: hamilton, bm
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3573198&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3573198&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    
    ********Sleeping for 50.813538789749146 seconds.********
    
    Now retrieving data for city #331: egvekinot, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=4031742&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=4031742&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #332: sur, om
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=286245&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=286245&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #333: torquay, gb
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2635650&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2635650&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #334: ust-nera, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2120048&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2120048&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #335: jiwani, pk
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1175712&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1175712&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #336: cobija, bo
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3919998&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3919998&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #337: sola, vu
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2134814&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2134814&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #338: kurilsk, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2123979&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2123979&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #339: lompoc, us
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=5367788&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=5367788&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #340: sangar, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2017215&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2017215&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #341: cherskiy, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2126199&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2126199&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #342: atar, mr
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2381334&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2381334&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #343: doaba, pk
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1179724&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1179724&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #344: solovetskiy, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=65.077429&lon=35.6383004&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=65.077429&lon=35.6383004&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #345: jiangyin, cn
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=31.920658&lon=120.284938&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=31.920658&lon=120.284938&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #346: celestun, mx
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3531368&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3531368&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #347: mar del plata, ar
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3430863&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3430863&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #348: general roca, ar
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3855065&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3855065&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #350: grand river south east, mu
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=-20.2888094&lon=57.78141199999999&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=-20.2888094&lon=57.78141199999999&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #351: tabiauea, ki
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=0.9182079999999999&lon=173.027965&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=0.9182079999999999&lon=173.027965&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #352: half moon bay, us
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=5354943&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=5354943&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #353: raglan, nz
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2183854&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2183854&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #354: kirovsk, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=548391&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=548391&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #356: vaitupu, wf
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=-13.2308863&lon=-176.1917035&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=-13.2308863&lon=-176.1917035&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #357: bradford, us
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=4608147&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=4608147&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #362: lincoln, us
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=5072006&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=5072006&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #375: tadine, nc
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2138285&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2138285&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #376: abatskoye, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1512210&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1512210&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #377: lasa, cn
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=29.65483799999999&lon=91.140552&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=29.65483799999999&lon=91.140552&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #378: byron bay, au
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2172880&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2172880&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    
    ********Sleeping for 50.742035150527954 seconds.********
    
    Now retrieving data for city #379: charyshskoye, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1508427&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1508427&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #380: muros, es
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=6357322&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=6357322&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #382: souillac, mu
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=933995&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=933995&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #383: tumkur, in
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1254089&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1254089&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #384: thurso, gb
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2635881&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2635881&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #385: doctor pedro p. pena, py
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=-22.45&lon=-62.34999999999999&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=-22.45&lon=-62.34999999999999&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #386: marcona, pe
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=-15.3439659&lon=-75.0844757&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=-15.3439659&lon=-75.0844757&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #387: east wenatchee bench, us
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=5793272&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=5793272&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #388: pomabamba, pe
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3693468&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3693468&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #389: grindavik, is
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3416888&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3416888&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #390: bontang, id
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1648186&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1648186&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #391: taraz, kz
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1516905&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1516905&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #392: waddan, ly
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2209055&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2209055&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #393: port hardy, ca
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=6111862&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=6111862&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #394: los llanos de aridane, es
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2514651&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2514651&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #395: mount isa, au
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2065594&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2065594&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #397: puerto del rosario, es
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=6360187&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=6360187&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #399: limoges, fr
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=6451740&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=6451740&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #401: morondava, mg
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1058381&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1058381&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #402: komsomolskiy, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=545728&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=545728&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #403: paltinis, ro
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=671427&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=671427&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #405: buta, cd
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=217570&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=217570&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #406: synya, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=485215&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=485215&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #407: moranbah, au
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=6533368&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=6533368&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #408: nantucket, us
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=4944903&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=4944903&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #409: homer, us
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=4273134&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=4273134&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #416: prince george, ca
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=6113365&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=6113365&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #417: georgetown, sh
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2411397&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2411397&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #418: laguna, br
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3459094&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3459094&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #419: brownsville, us
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=5234282&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=5234282&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    
    ********Sleeping for 50.95820069313049 seconds.********
    
    Now retrieving data for city #427: lithakia, gr
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=258241&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=258241&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #428: ust-karsk, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2013942&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2013942&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #429: termini imerese, it
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=6539140&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=6539140&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #431: luderitz, na
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3355672&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3355672&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #432: alofi, nu
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=4036284&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=4036284&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #433: sabratah, ly
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2212771&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2212771&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #434: yar-sale, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1486321&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1486321&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #435: clyde river, ca
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=5924351&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=5924351&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #436: mount gambier, au
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=7839440&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=7839440&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #438: halifax, ca
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=6324729&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=6324729&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #440: chicama, pe
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3698359&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3698359&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #441: owando, cg
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2255542&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2255542&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #442: isla mujeres, mx
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3526756&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3526756&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #443: huancabamba, pe
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3696466&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3696466&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #444: vilcun, cl
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3868210&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3868210&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #445: dingle, ie
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2964782&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2964782&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #446: yemelyanovo, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1486031&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1486031&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #447: fredericton, ca
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=5957776&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=5957776&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #448: tiksi, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2015306&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2015306&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #449: olenegorsk, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=515698&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=515698&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #450: gorno-chuyskiy, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=57.63204529999999&lon=111.7274595&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=57.63204529999999&lon=111.7274595&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #451: coihueco, cl
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3894406&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3894406&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #452: port hawkesbury, ca
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=6111867&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=6111867&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #453: miami, us
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=4164138&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=4164138&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #457: iklad, hu
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3051187&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3051187&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #458: smithers, ca
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=6149996&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=6149996&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #459: lisakovsk, kz
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1521315&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1521315&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #460: roseburg, us
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=5749352&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=5749352&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #461: svetlyy, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=831137&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=831137&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #466: tarudant, ma
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=30.4727126&lon=-8.8748765&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=30.4727126&lon=-8.8748765&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    
    ********Sleeping for 51.27017259597778 seconds.********
    
    Now retrieving data for city #467: odweyne, so
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=9.410198200000002&lon=45.06299019999999&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=9.410198200000002&lon=45.06299019999999&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #468: stykkisholmur, is
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3412888&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3412888&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #469: koungou, yt
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=7521430&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=7521430&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #471: demirci, tr
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=317241&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=317241&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #472: hukuntsi, bw
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=933726&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=933726&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #473: bamiantong, cn
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2038482&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2038482&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #474: kailua, us
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=5847486&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=5847486&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #475: talawdi, sd
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=10.6377926&lon=30.3839017&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=10.6377926&lon=30.3839017&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #476: cockburn town, tc
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3576994&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3576994&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #477: arraial do cabo, br
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3471451&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3471451&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #478: narrabri, au
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=7839755&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=7839755&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #480: ketchikan, us
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=5554428&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=5554428&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #481: acari, pe
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3948613&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3948613&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #482: tsihombe, mg
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=-25.3168473&lon=45.48630929999999&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=-25.3168473&lon=45.48630929999999&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #483: phan rang, vn
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=11.5825677&lon=108.9912066&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=11.5825677&lon=108.9912066&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #484: sisimiut, gl
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3419842&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3419842&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #485: linxia, cn
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1803331&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1803331&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #486: melville, ca
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=6071971&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=6071971&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #487: tumarbong, ph
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1680763&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1680763&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #488: norman wells, ca
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=6089245&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=6089245&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #489: west bend, us
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=5278422&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=5278422&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #490: gambela, et
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=337405&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=337405&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #491: gavle, se
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2712414&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2712414&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #492: sorland, no
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3137469&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3137469&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #493: tefe, br
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3661944&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3661944&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #494: privokzalnyy, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=58.875833&lon=60.72944390000001&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=58.875833&lon=60.72944390000001&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #495: quatre cocos, mu
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1106643&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1106643&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #496: kerema, pg
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2094144&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2094144&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #497: biak, id
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=-1.0381022&lon=135.9800848&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=-1.0381022&lon=135.9800848&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #498: funadhoo, mv
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1337620&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1337620&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    
    ********Sleeping for 50.909546852111816 seconds.********
    
    Now retrieving data for city #499: cavalcante, br
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3466594&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3466594&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #500: severodvinsk, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=496285&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=496285&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #501: princeton, ca
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=6113463&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=6113463&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #502: dwarka, in
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1272140&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1272140&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #503: ranong, th
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1150965&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1150965&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #504: monrovia, lr
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2274895&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2274895&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #505: pingdu, cn
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1798821&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1798821&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #509: belyy yar, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1510370&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1510370&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #511: hobyo, so
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=57000&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=57000&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #512: hovd, mn
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2030474&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2030474&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #515: belmonte, br
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3470137&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3470137&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #516: saint-pierre, pm
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3424934&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3424934&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #517: bathsheba, bb
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3374083&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3374083&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #518: isangel, vu
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2136825&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2136825&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #519: boa esperanca, br
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3469932&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3469932&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #521: merauke, id
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2082539&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2082539&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #522: trelew, ar
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3833883&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3833883&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #523: wulanhaote, cn
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?q=wulanhaote,cn&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?q=wulanhaote,cn&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Missing Current Weather Info for city #523: wulanhaote, cn
    Missing Forecast Info for city #523: wulanhaote, cn
    ---------------------------------------------------------------------------
    Now retrieving data for city #524: mataram, id
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1635882&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1635882&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #525: keningau, my
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1734098&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1734098&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #526: broken hill, au
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2173911&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2173911&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #527: saskylakh, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2017155&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2017155&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #528: anamur, tr
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=323828&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=323828&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #529: tura, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2014833&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2014833&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #530: honningsvag, no
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=779554&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=779554&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #531: shimoda, jp
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1852357&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1852357&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #532: saint-augustin, ca
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=6137462&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=6137462&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #533: francistown, bw
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=933778&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=933778&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #534: mayo, ca
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=6068416&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=6068416&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #535: morgan city, us
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=4333811&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=4333811&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    
    ********Sleeping for 50.970548152923584 seconds.********
    
    Now retrieving data for city #536: lima, pe
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3936456&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3936456&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #537: bolungarvik, is
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=66.1517719&lon=-23.261709&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=66.1517719&lon=-23.261709&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #538: nhamunda, br
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3393929&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3393929&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #539: abay, kz
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1526970&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1526970&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #540: almaznyy, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2027859&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2027859&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #542: san cristobal, ec
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3651949&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3651949&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #543: nanortalik, gl
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3421765&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3421765&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #544: haines junction, ca
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=5969025&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=5969025&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #545: havelock, us
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=4470244&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=4470244&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #546: athabasca, ca
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=5887916&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=5887916&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #547: kijang, id
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1640044&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1640044&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #548: flinders, au
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2166453&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2166453&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #552: beringovskiy, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2126710&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2126710&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #553: ko samui, th
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1154689&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1154689&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #554: sumter, us
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=4597948&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=4597948&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #555: trincomalee, lk
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1226260&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1226260&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #556: yarada, in
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1252783&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1252783&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #557: penzance, gb
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=7294638&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=7294638&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #559: buala, sb
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2109528&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2109528&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #560: nizhniy baskunchak, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=520798&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=520798&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #561: steinbach, ca
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=6156102&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=6156102&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #562: naze, jp
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1855540&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1855540&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #563: tonstad, no
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3134327&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3134327&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #564: paamiut, gl
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3421193&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3421193&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #565: tromso, no
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3133895&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3133895&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #566: jian, cn
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1806445&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1806445&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #568: aban, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1512218&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1512218&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #569: wanaka, nz
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2184707&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2184707&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #570: santa rosa, ar
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3428182&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3428182&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #573: mindelo, cv
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3374462&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3374462&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    
    ********Sleeping for 51.10153031349182 seconds.********
    
    Now retrieving data for city #574: protivin, cz
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3067395&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3067395&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #575: sivas, tr
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=300619&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=300619&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #577: skjervoy, no
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=777682&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=777682&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #578: sorong, id
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1626542&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1626542&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #579: saleaula, ws
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=-13.4482906&lon=-172.3367114&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=-13.4482906&lon=-172.3367114&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #580: rincon, an
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=32.2947732&lon=-81.2353612&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=32.2947732&lon=-81.2353612&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #581: canitas, mx
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=16.7861099&lon=-92.9111099&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=16.7861099&lon=-92.9111099&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #582: srandakan, id
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1626493&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1626493&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #583: hami, cn
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1529484&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1529484&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #584: son tay, vn
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1567621&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1567621&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #585: coquimbo, cl
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3893629&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3893629&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #586: bud, no
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=41.5337325&lon=-87.4994615&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=41.5337325&lon=-87.4994615&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #587: arcata, us
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=5558953&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=5558953&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #588: udachnyy, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2014624&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2014624&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #589: ardakan, ir
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=143073&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=143073&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #590: gohad, in
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1271083&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1271083&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #591: wad rawah, sd
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=364071&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=364071&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #592: inhambane, mz
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1045114&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1045114&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #593: kadykchan, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=63.083333&lon=147.05&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=63.083333&lon=147.05&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #594: comodoro rivadavia, ar
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3860443&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3860443&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #595: awjilah, ly
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=88533&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=88533&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #596: ayagoz, kz
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1525988&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1525988&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #597: clarence town, bs
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3572640&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3572640&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #598: inuvik, ca
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=5983607&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=5983607&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #599: ambilobe, mg
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1082243&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1082243&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #600: gamba, ga
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2400547&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2400547&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #601: casper, us
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=5820705&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=5820705&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #602: salinopolis, br
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3389822&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3389822&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #603: itarema, br
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=-2.9209642&lon=-39.91673979999999&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=-2.9209642&lon=-39.91673979999999&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #604: goundam, ml
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2456917&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2456917&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    
    ********Sleeping for 50.646607398986816 seconds.********
    
    Now retrieving data for city #605: bobo dioulasso, bf
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=11.1649219&lon=-4.3051542&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=11.1649219&lon=-4.3051542&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #606: tanggu, cn
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1793424&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1793424&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #607: natal, br
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3394023&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3394023&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #608: qandala, so
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=53157&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=53157&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #609: boende, cd
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=218680&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=218680&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #610: fernley, us
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=5504003&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=5504003&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #611: lolua, tv
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?q=lolua,tv&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?q=lolua,tv&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Missing Current Weather Info for city #611: lolua, tv
    Missing Forecast Info for city #611: lolua, tv
    ---------------------------------------------------------------------------
    Now retrieving data for city #612: buraydah, sa
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=107304&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=107304&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #613: dongkan, cn
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1812427&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1812427&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #614: kapit, my
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1737185&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1737185&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #615: carutapera, br
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3402648&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3402648&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #616: bow island, ca
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=5906757&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=5906757&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #617: povoa de varzim, pt
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2735787&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2735787&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #618: astrea, co
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3689458&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3689458&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #619: helong, cn
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2036933&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2036933&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #622: malatya, tr
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=304922&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=304922&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #624: anadyr, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2127202&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2127202&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #625: sarahan, in
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1257277&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1257277&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #626: wapi pathum, th
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1605072&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1605072&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #627: iqaluit, ca
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=5983720&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=5983720&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #628: rajkot, in
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1258847&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1258847&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #629: naron, es
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3115739&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3115739&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #630: pangnirtung, ca
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=6096551&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=6096551&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #631: atambua, id
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1651103&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1651103&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #632: santa cruz, cl
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3871616&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3871616&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #633: warqla, dz
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?q=warqla,dz&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?q=warqla,dz&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Missing Current Weather Info for city #633: warqla, dz
    Missing Forecast Info for city #633: warqla, dz
    ---------------------------------------------------------------------------
    Now retrieving data for city #634: honiara, sb
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2108502&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2108502&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #635: sooke, ca
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=6151264&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=6151264&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #636: loa janan, id
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1637510&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1637510&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #637: san carlos del zulia, ve
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3628489&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3628489&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    
    ********Sleeping for 50.97316575050354 seconds.********
    
    Now retrieving data for city #638: gallup, us
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=5468773&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=5468773&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #639: loralai, pk
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1171868&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1171868&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #640: muroto, jp
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1856392&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1856392&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #641: terrasini, it
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=6537752&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=6537752&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #642: sao felix do xingu, br
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3388847&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3388847&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #643: lar, ir
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=27.6741406&lon=54.3357845&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=27.6741406&lon=54.3357845&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #644: evanston, us
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=5824805&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=5824805&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #646: maracaju, br
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3457859&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3457859&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #647: sortland, no
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3137405&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3137405&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #648: tkibuli, ge
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=42.34141229999999&lon=42.994164&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=42.34141229999999&lon=42.994164&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #649: karratha, au
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=6620339&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=6620339&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #650: college, us
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=5859699&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=5859699&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #651: mandalgovi, mn
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2030065&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2030065&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #652: stoyba, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=52.7945943&lon=131.7095224&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=52.7945943&lon=131.7095224&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #653: waslala, ni
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3615745&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3615745&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #654: sysert, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1490402&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1490402&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #655: henties bay, na
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=-22.1134964&lon=14.2832038&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=-22.1134964&lon=14.2832038&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #656: west wendover, us
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=5710035&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=5710035&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #657: kieta, pg
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2094027&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2094027&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #658: quelimane, mz
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1028434&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1028434&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #659: ukiah, us
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=5404476&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=5404476&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #660: garowe, so
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=8.4084158&lon=48.4837239&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=8.4084158&lon=48.4837239&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #661: sawang daen din, th
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1606350&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1606350&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #662: chon daen, th
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1611106&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1611106&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #663: kudahuvadhoo, mv
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1337607&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1337607&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #664: birsk, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=576317&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=576317&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #665: gao, ml
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2457163&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2457163&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #666: yeppoon, au
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2142316&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2142316&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #667: oceanside, us
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=5129603&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=5129603&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #669: westport, nz
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2206900&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2206900&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    
    ********Sleeping for 50.667468547821045 seconds.********
    
    Now retrieving data for city #670: bairiki, ki
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=1.3290526&lon=172.9790528&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=1.3290526&lon=172.9790528&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #671: tilichiki, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2120591&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2120591&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #672: martinsicuro, it
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3173833&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3173833&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #673: qena, eg
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=26.155061&lon=32.7160121&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=26.155061&lon=32.7160121&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #674: businga, cd
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=217637&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=217637&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #675: viedma, ar
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3832899&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3832899&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #676: doha, kw
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=29.3155169&lon=47.8155695&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=29.3155169&lon=47.8155695&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #677: praia, cv
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3374333&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3374333&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #678: chifeng, cn
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2038067&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2038067&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #680: nassau, bs
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3571824&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3571824&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #681: stepnoye, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=487543&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=487543&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #683: barentu, er
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=342711&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=342711&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #684: pangai, to
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=4032369&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=4032369&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #685: mao, td
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2428394&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2428394&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #686: buin, pg
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=-6.7465002&lon=155.6851709&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=-6.7465002&lon=155.6851709&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #687: zhigalovo, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2012532&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2012532&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #688: lethem, gy
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=3.3663183&lon=-59.7977761&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=3.3663183&lon=-59.7977761&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #689: karaul, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=70.070114&lon=83.23083489999999&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=70.070114&lon=83.23083489999999&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #690: arlit, ne
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2447513&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2447513&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #691: andevoranto, mg
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=-18.9549753&lon=49.1082407&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=-18.9549753&lon=49.1082407&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #692: charters towers, au
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=7839570&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=7839570&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #694: bacuit, ph
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=11.2097089&lon=119.4622539&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=11.2097089&lon=119.4622539&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #695: yarim, ye
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=69559&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=69559&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #696: mogadishu, so
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=53654&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=53654&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #697: bonavista, ca
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=5905393&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=5905393&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #698: jinchang, cn
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1805733&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1805733&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #701: kuppam, in
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1265555&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1265555&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #702: kodinar, in
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1266397&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1266397&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #703: saldanha, za
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3361934&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3361934&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #704: tricase, it
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=6540769&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=6540769&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    
    ********Sleeping for 51.32037305831909 seconds.********
    
    Now retrieving data for city #706: narva-joesuu, ee
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=590030&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=590030&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #707: halalo, wf
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=-13.3436344&lon=-176.2171202&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=-13.3436344&lon=-176.2171202&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #708: petropavlovsk-kamchatskiy, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2122104&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2122104&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #709: san carlos de bariloche, ar
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3837856&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3837856&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #711: sarmanovo, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=498537&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=498537&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #712: huarmey, pe
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3939168&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3939168&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #713: ajtos, bg
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=42.7031175&lon=27.250644&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=42.7031175&lon=27.250644&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #714: prata, br
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3452440&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3452440&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #715: vardo, no
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=777019&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=777019&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #716: anniston, us
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=4830198&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=4830198&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #717: sulangan, ph
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1685422&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1685422&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #720: batagay, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2027044&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2027044&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #721: mnogovershinnyy, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2019935&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2019935&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #722: pitimbu, br
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3391889&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3391889&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #723: pisco, pe
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3932145&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3932145&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #724: dera bugti, pk
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1180295&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1180295&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #725: jijiga, et
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=333795&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=333795&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #726: la quinta, us
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=5364079&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=5364079&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #727: tungkang, tw
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=22.4654087&lon=120.4536281&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=22.4654087&lon=120.4536281&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #728: las palmas, es
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=28.1235459&lon=-15.4362574&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=28.1235459&lon=-15.4362574&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #729: koslan, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=544084&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=544084&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #730: kautokeino, no
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=779327&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=779327&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #732: kostino, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=543939&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=543939&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #739: manta, ec
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3654410&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3654410&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #740: aksarayskiy, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=583683&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=583683&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #741: port moresby, pg
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2088122&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2088122&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #742: iranshahr, ir
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1160939&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1160939&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #743: naral, bd
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?lat=43.548508&lon=-96.722286&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?lat=43.548508&lon=-96.722286&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #744: port keats, au
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=2063039&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=2063039&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #745: kodinsk, ru
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=1503037&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=1503037&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    
    ********Sleeping for 51.19490933418274 seconds.********
    
    Now retrieving data for city #746: martin, sk
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3058780&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3058780&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #747: pedernales, do
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=3495137&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=3495137&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    Now retrieving data for city #748: fare, pf
    Current Weather URL:
    https://api.openweathermap.org/data/2.5/weather?id=4034496&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    Forecast Weather URL:
    https://api.openweathermap.org/data/2.5/forecast?id=4034496&APPID=ec80582a424f72b1c1b29ba4f3195397&units=imperial
    ---------------------------------------------------------------------------
    


```python
# Summary Report
print("Counts and Errors Report")
print('---------------------------------------------------------------------------')
print("Count")
print('----------------')
print(str(counter))
print('---------------------------------------------------------------------------')
print("Errors")
print('----------------')
print('# of Current Weather Errors: ' + str(cur_errors))
print("Current Weather Errors Index List:")

if len(cur_err_list) > 0:
    for n in cur_errors:
        print(n)
else:
    print('None')
print("")
print('# of Forecast Weather Errors:' + str(for_errors))
print("Forecast Weather Errors Index List: ")
if len(for_err_list) > 0:
    for n in for_errors:
        print(n)
else:
    print('None')
print('---------------------------------------------------------------------------')
```

    Counts and Errors Report
    ---------------------------------------------------------------------------
    Count
    ----------------
    603
    ---------------------------------------------------------------------------
    Errors
    ----------------
    # of Current Weather Errors: 4
    Current Weather Errors Index List:
    


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    <ipython-input-180-4fbfdcae8c62> in <module>()
         12 
         13 if len(cur_err_list) > 0:
    ---> 14     for n in cur_errors:
         15         print(n)
         16 else:
    

    TypeError: 'int' object is not iterable



```python
#view columns
weather_data.columns
```




    Index(['city', 'country', 'coord', 'id', 'lat', 'lng', 'cur_date', 'cur_temp',
           'cur_humidity', 'cur_clouds', 'cur_wind', 'max_date', 'max_temp',
           'max_temp_humidity', 'max_temp_clouds', 'max_temp_wind', 'avg_date0',
           'avg_date1', 'avg_temp', 'avg_humidity', 'avg_clouds', 'avg_wind'],
          dtype='object')




```python
# clean up
clean_col = weather_data.columns[4:]
clean_col
```




    Index(['lat', 'lng', 'cur_date', 'cur_temp', 'cur_humidity', 'cur_clouds',
           'cur_wind', 'max_date', 'max_temp', 'max_temp_humidity',
           'max_temp_clouds', 'max_temp_wind', 'avg_date0', 'avg_date1',
           'avg_temp', 'avg_humidity', 'avg_clouds', 'avg_wind'],
          dtype='object')




```python
#loop throught to clean columns to be able to use for graphs
for c in clean_col:
    weather_data[c] = pd.to_numeric(weather_data[c], errors = 'coerce') 
    weather_data = weather_data[weather_data[c].isnull() == False]

len(weather_data)
```




    599




```python
# check weather data types
weather_data.dtypes
```




    city                  object
    country               object
    coord                 object
    id                     int64
    lat                  float64
    lng                  float64
    cur_date               int64
    cur_temp             float64
    cur_humidity           int64
    cur_clouds             int64
    cur_wind             float64
    max_date               int64
    max_temp             float64
    max_temp_humidity      int64
    max_temp_clouds        int64
    max_temp_wind        float64
    avg_date0              int64
    avg_date1              int64
    avg_temp             float64
    avg_humidity         float64
    avg_clouds           float64
    avg_wind             float64
    dtype: object




```python
#Export to csv
weather_data.to_csv('Data_Output/clean_weather_data.csv')
```


```python
########## Data CSV read to avoid pull requests again  ########
weather_data = pd.read_csv('Data_Output/clean_weather_data.csv')
weather_data.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Unnamed: 0</th>
      <th>city</th>
      <th>country</th>
      <th>coord</th>
      <th>id</th>
      <th>lat</th>
      <th>lng</th>
      <th>cur_date</th>
      <th>cur_temp</th>
      <th>cur_humidity</th>
      <th>...</th>
      <th>max_temp</th>
      <th>max_temp_humidity</th>
      <th>max_temp_clouds</th>
      <th>max_temp_wind</th>
      <th>avg_date0</th>
      <th>avg_date1</th>
      <th>avg_temp</th>
      <th>avg_humidity</th>
      <th>avg_clouds</th>
      <th>avg_wind</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>adrar</td>
      <td>dz</td>
      <td>{'lon': -0.29388000000000003, 'lat': 27.87429}</td>
      <td>2508813</td>
      <td>27.87</td>
      <td>-0.29</td>
      <td>1517040000</td>
      <td>48.20</td>
      <td>45</td>
      <td>...</td>
      <td>66.69</td>
      <td>28</td>
      <td>0</td>
      <td>15.46</td>
      <td>1517043600</td>
      <td>1517464800</td>
      <td>64.72325</td>
      <td>39.000</td>
      <td>51.9</td>
      <td>12.83450</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>barrow</td>
      <td>us</td>
      <td>{'lon': -156.788727, 'lat': 71.290581}</td>
      <td>5880054</td>
      <td>71.29</td>
      <td>-156.79</td>
      <td>1517039580</td>
      <td>-23.81</td>
      <td>90</td>
      <td>...</td>
      <td>-8.43</td>
      <td>100</td>
      <td>56</td>
      <td>15.37</td>
      <td>1517043600</td>
      <td>1517464800</td>
      <td>-3.74725</td>
      <td>92.600</td>
      <td>36.8</td>
      <td>12.40175</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>palmer</td>
      <td>us</td>
      <td>{'lon': -98.257294, 'lat': 41.22224}</td>
      <td>5074769</td>
      <td>41.22</td>
      <td>-98.26</td>
      <td>1517040900</td>
      <td>30.22</td>
      <td>86</td>
      <td>...</td>
      <td>39.23</td>
      <td>89</td>
      <td>0</td>
      <td>7.00</td>
      <td>1517043600</td>
      <td>1517464800</td>
      <td>24.12625</td>
      <td>80.900</td>
      <td>29.5</td>
      <td>8.51000</td>
    </tr>
    <tr>
      <th>3</th>
      <td>6</td>
      <td>punta arenas</td>
      <td>cl</td>
      <td>{'lon': -70.916672, 'lat': -53.150002}</td>
      <td>3874787</td>
      <td>-53.15</td>
      <td>-70.92</td>
      <td>1517040000</td>
      <td>51.80</td>
      <td>62</td>
      <td>...</td>
      <td>53.20</td>
      <td>82</td>
      <td>8</td>
      <td>17.92</td>
      <td>1517043600</td>
      <td>1517464800</td>
      <td>48.32350</td>
      <td>92.375</td>
      <td>50.0</td>
      <td>20.57275</td>
    </tr>
    <tr>
      <th>4</th>
      <td>7</td>
      <td>rosario</td>
      <td>br</td>
      <td>{'lon': -44.2493388, 'lat': -2.9410215}</td>
      <td>0</td>
      <td>-2.94</td>
      <td>-44.25</td>
      <td>1517040000</td>
      <td>77.00</td>
      <td>88</td>
      <td>...</td>
      <td>81.22</td>
      <td>91</td>
      <td>68</td>
      <td>7.29</td>
      <td>1517043600</td>
      <td>1517464800</td>
      <td>78.60200</td>
      <td>93.225</td>
      <td>52.6</td>
      <td>5.27425</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 23 columns</p>
</div>




```python
#date sorting and conversions dictionary for graph labels

dates = {'max_cur': weather_data['cur_date'].max(),
         'min_cur': weather_data['cur_date'].min(),
         'max_max': weather_data['max_date'].max(),
         'min_max': weather_data['max_date'].min(),
         'min_avg': weather_data['avg_date0'].max(),
         'max_avg': weather_data['avg_date1'].min()
        }

for key in dates.keys():
    convert = datetime.utcfromtimestamp(dates[key]).strftime('%Y %m %d %I:%M:%S %p')
    dates[key] = convert
```


```python
# dictionary for labels
labels_dic = {"cur_temp": "Current Temperature", 
              'max_temp': 'Maximum Temp 24 Hours', 
              'avg_temp': 'Average Forecasted Temp in 5 Days',
             'cur_humidity': 'Current Humidity',
             'max_temp_humidity': "Forecasted Humidity (%) at the Maximum Temperature in 24 Hours",
             'avg_humidity': 'Average Forecasted Humidity (%) over 5 Days',
             'cur_clouds': 'Current Cloud Cover (%)',
             'max_temp_clouds': 'Forecasted Cloud Cover (%) at the Maximum Forecasted Temperature in 24 Hours',
             'avg_clouds': 'Average Forecasted Cloud Cover (%) over 5 Days',
             'cur_wind': 'Current Wind Speed (mph)',
             'max_temp_wind': 'Forecasted Wind Speed (mph) at the Maximum Forecasted Temperature in 24 Hours',
             'avg_wind': 'Average Forecasted Wind Speed (mph) over 5 Days'}
```


```python
# Temp vs Latitude Graphs
temp_list = ['cur_temp', 'max_temp', 'avg_temp']  #would have done only dict but wanted consistent order.

xvals = weather_data['lat']

for temp in temp_list:
    # y values of each item in list for separate graphs
    yvals = weather_data[temp]
    #adds title including title and timestamp range of sample data
    plt.title("%s vs Latitude \n Samples Taken from %s to %s UTC" % (labels_dic[temp], dates['min_' + temp.split('_')[0]],  dates['max_' + temp.split('_')[0]]))
    plt.axvline(0, color = 'black', alpha = .25, label = 'Equator') #adds equator line
    plt.text(1,30,'Equator',rotation=90)
    plt.ylim(15, 120) #to give consistent scale
    plt.xlabel('Latitude')
    plt.ylabel("Temperature (F)")
    plt.scatter(xvals, yvals)
    plt.show()
    plt.savefig("Graph_Output/%s vs Latitude.png" % (labels_dic[temp]))
```


![png](output_34_0.png)



![png](output_34_1.png)



![png](output_34_2.png)



```python
# Humidity vs Latitude Graphs
#see first set of graphs commenting for notes
hum_list = ['cur_humidity', 'max_temp_humidity', 'avg_humidity']  #would have done only dict but wanted consistent order.

xvals = weather_data['lat']

for hum in hum_list:
    yvals = weather_data[hum]
    plt.title("%s vs Latitude \n Samples Taken from %s to %s UTC" % (labels_dic[hum], dates['min_' + hum.split('_')[0]],  dates['max_' + hum.split('_')[0]]))
    plt.xlabel('Latitude')
    plt.ylabel('Humidity (%)')
    plt.axvline(0, color = 'black', alpha = .25, label = 'Equator')
    plt.text(1,20,'Equator',rotation=90)
    plt.scatter(xvals, yvals)
    plt.show()
    plt.savefig("Graph_Output/%s vs Latitude.png" % (labels_dic[hum]))
```


![png](output_35_0.png)



![png](output_35_1.png)



![png](output_35_2.png)



```python
# Cloud Cover vs Latitude Graphs
#see first set of graphs commenting for notes
cloud_list = ['cur_clouds', 'max_temp_clouds', 'avg_clouds']  #would have done only dict but wanted consistent order.

xvals = weather_data['lat']

for clo in cloud_list:
    yvals = weather_data[clo]
    plt.title("%s vs Latitude \n Samples Taken from %s to %s UTC" % (labels_dic[clo], dates['min_' + clo.split('_')[0]],  dates['max_' + clo.split('_')[0]]))
    plt.xlabel('Latitude')
    plt.ylabel('Cloud Cover (%)')
    plt.ylim(-5,105)
    plt.axvline(0, color = 'black', alpha = .25, label = 'Equator')
    plt.text(-5,-20,'Equator')
    plt.scatter(xvals, yvals)
    plt.show()
    plt.savefig("Graph_Output/%s vs Latitude.png" % (labels_dic[clo]))
```


![png](output_36_0.png)



![png](output_36_1.png)



![png](output_36_2.png)



```python
# Wind Speed vs Latitude Graphs
#see first set of graphs commenting for notes
win_list = ['cur_wind', 'max_temp_wind', 'avg_wind']  #would have done only dict but wanted consistent order.

xvals = weather_data['lat']

for win in win_list:
    yvals = weather_data[win]
    plt.title("%s vs Latitude \n Samples Taken from %s to %s UTC" % (labels_dic[win], dates['min_' + win.split('_')[0]],  dates['max_' + win.split('_')[0]]))
    plt.xlabel('Latitude')
    plt.ylabel('Wind Speed (mph))')
    plt.ylim(-5,60)
    plt.axvline(0, color = 'black', alpha = .25, label = 'Equator')
    plt.text(1,35,'Equator',rotation=90)
    plt.scatter(xvals, yvals)
    plt.show()
    plt.savefig("Graph_Output/%s vs Latitude.png" % (labels_dic[win]))
```


![png](output_37_0.png)



![png](output_37_1.png)



![png](output_37_2.png)



```python
#graphs lats vs long, temperature scale from red(hot) to green(cool), and bubble size based on humidity, cloud cover, and wind speed
xvars = weather_data['lng']
yvars = weather_data['lat']
color = weather_data['avg_temp']
size_list = ['avg_humidity', 'avg_clouds', 'avg_wind']

#loops through size list and only changes size of bubbles based on different variables
for measure in size_list:  
    plt.figure(figsize = (18,12))
    plt.xlim(-180,180)
    plt.ylim(-90,90)
    plt.title("Global Temperatures Based on 5 Day Average \n Samples taken from %s to %s UTC \n Note:  Bubble Size Corresponds to %s" % (dates['min_avg'], dates['max_avg'], labels_dic[measure]))
    plt.axhline(0, color = 'black', alpha = .25, label = 'Equator')
    plt.text(-155,3,'Equator')
    size = weather_data[measure]
    plt.scatter(xvars, 
                yvars, 
                c = color, 
                s = size * 6, 
                edgecolor = 'black', 
                linewidth = 1, 
                alpha = .5, 
                cmap=plt.cm.RdYlGn_r)
    plt.show()
    plt.savefig("Graph_Output/Global Temperatures Based on 5 Day Average Bubble Plot: %s.png" % (measure))
```


    <matplotlib.figure.Figure at 0x17bb9712198>



![png](output_38_1.png)



    <matplotlib.figure.Figure at 0x17bb9637b00>



![png](output_38_3.png)



    <matplotlib.figure.Figure at 0x17bb953c780>



![png](output_38_5.png)

