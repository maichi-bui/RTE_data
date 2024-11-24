import argparse
from datetime import datetime, timedelta

from utils.common_func import get_access_token, get_data, dt_isoformat, process_raw_data
from utils.config import HOST_NAME, BASE, BASE64_CLIENT

oauth_url = f"https://{HOST_NAME}/token/oauth/ HTTP/1.1"
generation_forecast_url = f"https://{HOST_NAME}{BASE}/forecasts"

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--end_date', default=datetime.now(), type=lambda dt: datetime.strptime(dt, '%Y-%m-%d %H:%M:%S'),
                        help='end of forecast period')
    
    parser.add_argument('--interval', default=30,
                        help='query interval from now (in minutes)')
    
    args = parser.parse_args()
    args.end_date = args.end_date + (datetime.min - args.end_date) % timedelta(minutes=30)
    start_date = args.end_date - timedelta(minutes=args.interval)
    date_query = {'start_date' : dt_isoformat(start_date), 'end_date' : dt_isoformat(args.end_date)}

    # get access token
    access_token = get_access_token(oauth_url)
    data_res = get_data(generation_forecast_url, access_token, params = date_query, encode_dt_param=True)
    processed_data = process_raw_data(data_res)

    processed_data.to_csv('updated_bihour_forecast.csv', index=False)
    