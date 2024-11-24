import os
import json
from dotenv import load_dotenv, dotenv_values 

load_dotenv() 


with open('generation_forecast_v2.1.json', 'r') as file:
    swaggeer_api = json.load(file)

HOST_NAME = swaggeer_api['host']
BASE = swaggeer_api['basePath']
SCHEME = swaggeer_api['schemes'][0]
BASE64_CLIENT = os.getenv('BASE64_CLIENT')
FORECAST_SECTOR = ['AGGREGATED_PROGRAMMABLE_FRANCE','AGGREGATED_NON_PROGRAMMABLE_FRANCE', 'WIND_ONSHORE','WIND_OFFSHORE', 'SOLAR', 'AGGREGATED_CPC', 'MDSETRF', 'MDSESTS']
FORECAST_TYPE = ['CURRENT','ID','D-1','D-2','D-3']