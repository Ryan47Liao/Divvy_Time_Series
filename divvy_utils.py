"""_summary_
This Module contains visualization tools for Geographic Travel Time Series Analysis 

@Author: Ryan47Liao
@Date: 2022/05/26
"""

from re import M
import pandas as pd 
import matplotlib.pyplot as plt
import os
import numpy as np
from datetime import datetime
import csv
import matplotlib.pyplot as plt
from pyrsistent import m
import seaborn as sns
from tqdm.notebook import trange, tqdm
from datetime import datetime,timedelta
import random
from pygeocoder import Geocoder
import folium
import branca.colormap as cmp
from prettytable import PrettyTable as pt


class TS_divvy:
    def __init__(self,df_station,df_TS):
        self._df_station = df_station 
        self._df_TS = df_TS
    
    def Geo_Viz(self, col, 
                df_station = None, categorical = False, 
                color_palette = 'rocket',colormap = None, color_dct=None,
                color_map_caption='Color Scale for Map',
                lower_scale = 'min', upper_scale = '75%', 
                Init_COORDINATES = (41.864073, -87.706819)):
        """Generating an interactive map to visualize stations, color code the specified feature given color schema 

        Args:
            df_station (pd.DataFrame): The typical df_station table that contains station_name,coordinates,NbhID and other features
            categorical (bool, optional): Weather the color coded feature is categorical. Defaults to False.
            col (_type_): The column to be colocoded onto the stations 
            color_palette (str, optional): The seaborn color schema for visualizing continous variable. Defaults to 'rocket'.
            colormap (_type_, optional): _description_. Defaults to None.
            color_map_caption (str, optional): The caption for the color scale, this only appears for continous feature. Defaults to 'Color Scale for Map'.
            lower_scale (str, optional): the lower cap for color scheme. Defaults to 'min'.
            upper_scale (str, optional): _description_. The upper cap for color scheme. Defaults to '75%'.
            Init_COORDINATES (tuple, optional): _description_. Defaults to (41.864073, -87.706819), which is Chicago's corrdinate

        Returns:
            _type_: _description_
        """
        def get_popUp(row):
            html = pd.DataFrame(row).to_html()  
            iframe = folium.IFrame(html)
            popup = folium.Popup(iframe, min_width=300, max_width=300)
            return popup

        if df_station is None:
            df_station = self._df_station
            
        if str(df_station.dtypes[col]) == 'object':
            print(f"Non Numerical feature identified, autocorrecting {col} to Categorical data")
            categorical = True 
            
        if colormap is None:
            if categorical:
                if color_dct is None:
                    colors = ["red", "blue", "green", "purple", "orange", "darkred",
                    "darkblue", "darkgreen", "cadetblue", "darkpurple", "pink", "gray", "black"]
                    colors_subset = random.sample(colors,k=len(df_station[col].unique()))
                    #print(colors_subset)
                    color_dct = {i:j for i,j in zip(df_station[col].unique(),colors_subset)}
                print(f'color_dct:{color_dct}')
                cat_legend = str(color_dct)[1:-1]
                colormap = lambda x: color_dct[x]
            else:
                colormap = cmp.StepColormap(
                eval(sns.color_palette(color_palette).as_hex().__str__()),
                vmin=df_station[col].describe()[lower_scale], vmax=df_station[col].describe()[upper_scale],
                #for change in the colors, not used fr linear
                caption= color_map_caption    #Caption for Color scale or Legend
                ) 
                

        # create empty map zoomed in on San Francisco
        map = folium.Map(location=Init_COORDINATES, zoom_start=11)
        
        # add a marker for every record in the filtered data
        for idx,row in df_station.iterrows():
            folium.Circle(
                location = (row['lat'],row['lng']),
                radius = 2,
                popup = get_popUp(row),#
                color = colormap(row[col])
                ).add_to(map)
        if categorical:
            title_html = '''
                        <h3 align="center" style="font-size:16px"><b>{}</b></h3>
                        '''.format(cat_legend)   
            map.get_root().html.add_child(folium.Element(title_html))
        else:
            map.add_child(colormap)
        return map

    def Forecastability_Analysis(self,ts_sample=None):
        """Analysis the forecastability of a Time Series Panel Data 

        Args:
            ts_sample (_type_, optional): _description_. Defaults to None.

        Returns:
            pd.DataFrame: _description_
        """
        if ts_sample is None:
            ts_sample = self._df_TS.copy()
        ##Calculating ADI
        adi = ts_sample.shape[0] / (ts_sample != 0).sum(axis=0)
        #Calculating CV2
        avg_ = np.average(ts_sample,axis=0)
        std_ = np.std(ts_sample,axis=0).values
        cv2 = (std_/avg_)**2
        #Return output 
        out_dct = {'stations':list(ts_sample.columns),'ADI':adi,'CV2':cv2}
        temp_ = pd.DataFrame(out_dct).reset_index(drop=True)
        temp_.insert(temp_.shape[1],'forecastability', (temp_.ADI < 1.32).apply(lambda x:str(1*x)) + (temp_.CV2 < 0.49).apply(lambda x:str(1*x)))
        f_mapper = {'11':'Smooth','10':'Erratic','01':'Intermittent','00':'Lumpy'}
        temp_.forecastability = temp_.forecastability.apply(lambda x:f_mapper[x])
        return temp_

    def Forecastability_Visualization(self,col,ts_sample=None,merge_on = 'station_name'):
        FA_res = self.Forecastability_Analysis(ts_sample)
        df_station_agg = self._df_station.merge(FA_res.rename({'stations':merge_on},axis=1),how='left')
        df_station_agg = df_station_agg.dropna(subset=['lng','lat',col]) 
        return self.Geo_Viz(col,df_station_agg)
    
if __name__ == '__main__':
    df_station = pd.read_csv('E:\Data\divvy/df_station_1721_FINAL.csv',index_col=0)
    #df_ts_out_1721_Station_Daily = pd.read_csv('E:\Data\divvy\TimeS/df_ts_out_1721_Station_Daily.csv',index_col=0)
    df_ts_in_1721_Station_Daily = pd.read_csv('E:\Data\divvy\TimeS/df_ts_in_1721_Station_Daily.csv',index_col=0)
    TS_EDA_IN_Station_Daily = TS_divvy(df_station,df_ts_in_1721_Station_Daily)
    TS_EDA_IN_Station_Daily_res = TS_EDA_IN_Station_Daily.Forecastability_Analysis()
    print(TS_EDA_IN_Station_Daily_res.forecastability.value_counts())
    
    merge_on = 'station_name'
    col = 'forecastability'
    df_station_agg = df_station.merge(TS_EDA_IN_Station_Daily_res.rename({'stations':merge_on},axis=1),how='left')
    df_station_agg = df_station_agg.dropna(subset=['lng','lat',col])
    
    map = TS_EDA_IN_Station_Daily.Geo_Viz(col,df_station_agg,categorical=True)
    map.save('E:\Data\divvy\Maps/test_map.html')
