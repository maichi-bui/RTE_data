import requests
import pandas as pd
from zoneinfo import ZoneInfo
from urllib.parse import urlencode
from datetime import datetime
from utils.config import BASE64_CLIENT



def get_access_token(oauth_url, payload = {} , headers=None):
    """Calling API to get access token for data retrieveing later

    Args:
        oauth_url (str)
        payload (dict, optional): Defaults to {}.
        headers (_type_, optional): Defaults to None.

    Returns:
        access_token
    """
    payload = {}
    headers = {
    'Authorization': f'Basic {BASE64_CLIENT}'
    }
    
    try:
        response = requests.request("POST", oauth_url, headers=headers, data=payload, timeout=300)
         # Raise an exception for HTTP errors
        response.raise_for_status()
        access_token = response.json()['access_token']
        if not access_token:
            print("Access token not found in response!")
            return None
        
        print("Access token retrieved successfully.")
        return access_token
    
    except requests.exceptions.RequestException as e:
        print(f"Error getting access token: {e}")
        return None

def get_data(url, access_token,headers={}, params=None, encode_dt_param=False):
    """Calling API to get data

    Args:
        url (_type_): _description_
        access_token (_type_): _description_
        headers (dict, optional): _description_. Defaults to {}.
        params (_type_, optional): _description_. Defaults to None.
        encode_dt_param (bool, optional): _description_. Defaults to False.

    Returns:
        data
    """
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
        }
    if encode_dt_param:
        params = urlencode(params, safe=':') # encode start_date & end_date params
    try:
        response = requests.request("GET", url, headers=headers, params=params, timeout=300)
        response.raise_for_status()
        
        data = response.json()
        if data: 
            print('Forecast data fetched successfully.')
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def dt_isoformat(dt):
    """
    Encodes a datetime object in the format "YYYY-MM-DDTHH:MM:SS%2BHH:MM".

    Parameters:
    - dt (datetime): The datetime object to encode.
    
    Returns:
    - encoded_dt: Encoded query parameter string.
    """
    dt_tz = dt.astimezone(ZoneInfo("Europe/Paris")).isoformat()
    
    return dt_tz

class DuplicatedKey(Exception):
    pass

def process_raw_data(forecast_raw: dict):
    """Flatten data retrieved from calling API

    Args:
        forecast_raw (dict): raw data response from API

    Raises:
        DuplicatedKey: _description_

    Returns:
        flattened_data: data that has been processed and flattened
    """
    forecast_data = pd.DataFrame(forecast_raw['forecasts'])
    # identifier: combination of ['production_type','type','sub_type'] subtype for: AGREGEE_PO; MDSETRF; MDSESTS
    
    if 'sub_type' in forecast_data.columns:
        forecast_data.sub_type = forecast_data.sub_type.fillna("na")
        identifier = ['production_type','type','sub_type']
    else:
        identifier = ['production_type','type']

    check_unique = forecast_data.groupby(identifier).count()
    
    if check_unique[check_unique != 1].stack().sum() > 0:
        dup_keys = check_unique[check_unique > 1].dropna().to_dict('split')['index']
        raise DuplicatedKey(f'Data contain multiple forecasts for one sector: {dup_keys}')
        
    
    forecast_data['start_date'] = forecast_data['start_date'].apply(datetime.fromisoformat)
    forecast_data['end_date'] = forecast_data['end_date'].apply(datetime.fromisoformat)
    forecast_data = forecast_data.rename(columns={'start_date':'start_query_date','end_date':'end_query_date'})
    forecast_data = forecast_data.groupby(identifier).first().reset_index().explode('values')
    no_forecast = forecast_data[forecast_data['values'].apply(lambda x: isinstance(x, dict)==False)]

    if len(no_forecast) > 0:
        print(f'no forecast for {no_forecast.production_type.unique()}')

    forecast_data = forecast_data[forecast_data['values'].apply(lambda x: isinstance(x, dict))]
    flattened_data = pd.concat([forecast_data['values'].apply(pd.Series), forecast_data.drop('values', axis=1)], axis=1)
    flattened_data = pd.concat([flattened_data, no_forecast.rename(columns={'values':'value'})]).reset_index(drop=True)
    # flattened_data['start_date'] = flattened_data['start_date'].apply(datetime.fromisoformat)
    # flattened_data['end_date'] = flattened_data['end_date'].apply(datetime.fromisoformat)
    return flattened_data