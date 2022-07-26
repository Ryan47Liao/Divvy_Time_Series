# Divvy Bikes Stock Rebalancing Issues
## Time Series Approach

Help Divvy, a Chicago based bike-sharing company, solve their bike rebalancing challenges. 

As people’s usage of traditional commuting plumed since the onset of covid, bike-sharing services such as divvy have become increasingly popular. Demand for bikes are not evenly distributed, this leads to either bike shortage or lack of empty docks. This individual project visualized this challenge and proposed a solution to the problem.

**Use Case:**
- Predicting potential station/dock availability using bike-in and bike-out data as proxies

**Dataset:**  
https://www.kaggle.com/datasets/leonidasliao/divvy-station-dock-capacity-time-series-forecast

https://ride.divvybikes.com/system-data
- Divvy Bikes Travel History
- Bike-in and Bike-out

https://www.visualcrossing.com/weather/weather-data-services
- Weather History

**Period:**
2017-2021

**Goals:**
- Realtime Hourly Forecast
- Aggregated Daily Forecast

**Key Challenges:**
- Lumpy/Erratic Data
- Complex seasonality (more than two seasonalities)
- High Variance

**Models:**

Univariate Forecasting
1. TBATS
2. Double-Seasonal Holt-Winters
3. Auto Arima with Fourier Terms
4. Prophet

**Intervention Examination (Covid-19 Effect):**
1. Dynamic Regression (incorporating weather to see Covid impact)
2. Causal impact, intervention model

**Result:**
1. Best model: TBATS using two seasonalities (yearly, weekly)
2. Covid-19 impact can be seen by incorporating weather data as weather provides contrast to traffic data (weather not affected by Covid while Divvy traffic was. Covid-19 also impacts various regions differently).
