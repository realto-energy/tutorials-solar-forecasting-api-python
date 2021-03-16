### Tutorial: Visualising solar forecast data using Python and web APIs
## by re.alto energy -> https://portal.realto.io
# This script uses the Elia Belgian Solar Forecasting API ->
# https://portal.realto.io/browse-apis/elia-solar-forecasting-be/details

# imports

import requests
import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns

# inputs

token = 'YOUR_API_TOKEN_HERE' # from https://portal.realto.io
endpoint = 'https://api.realto.io/elia-sf-BE/GetChartDataForZone'
sourceId = 1 # 1 = Belgium
dateFrom = '2021-03-07'
dateTo = '2021-03-15'

# call API and set-up DataFrame

response = requests.get(endpoint, headers={'OCP-Apim-Subscription-Key': token}, params={'dateFrom':dateFrom, 'dateTo':dateTo, 'sourceId':sourceId})
json = response.json()
data = json['SolarForecastingChartDataForZoneItems']
df = pd.DataFrame(data)

# create timestamps

dates = []

for index, row in df.iterrows():
  dates.append(pd.to_datetime(re.findall("\d+", row['StartsOn']['DateTime'])[0], unit='ms'))
 
df['DateTime'] = dates

# visualising

new_df = df[['WeekAheadForecast', 'DayAheadForecast', 'MostRecentForecast', 'RealTime', 'DateTime']]
new_df.set_index('DateTime', inplace=True)
sns.set_style("darkgrid")
fig, ax = plt.subplots(figsize=(10, 10))
sns.lineplot(data=new_df, ax=ax, palette="tab10", linewidth=2.5)
