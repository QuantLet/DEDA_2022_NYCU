#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 12:39:50 2022

@author: youcefnazimtahari
"""

import requests 
import json 
import pprint
import pandas as pd
response = requests.get("https://data.ntpc.gov.tw/api/datasets/71CD1490-A2DF-4198-BEF1-318479775E8A/json") 
content = response.content
json_tree = json.loads(content)
pprint.pprint(json_tree)

for bike_rent_records in json_tree:
    leftRatio = float(bike_rent_records["sbi"]) / float(bike_rent_records["tot"]) * 100
    print("ID:{0} Left:{2:0.1f}% Name:{1}".format(bike_rent_records["sno"], bike_rent_records["aren"], leftRatio))
    
bike_rent_records['sbi'].plot()