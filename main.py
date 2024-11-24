import argparse
from datetime import datetime, timedelta

from utils.common_func import get_access_token, get_data, dt_isoformat, process_raw_data
from utils.config import HOST_NAME, BASE

oauth_url = f"https://{HOST_NAME}/token/oauth/ HTTP/1.1"
generation_forecast_url = f"https://{HOST_NAME}{BASE}/forecasts"

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--end_date', default=datetime.now(), type=lambda dt: datetime.strptime(dt, '%Y-%m-%d %H:%M:%S'),
                        help='end of forecast period')
    
    parser.add_argument('--interval', default=2,
                        help='query interval from now (in days)')
    args = parser.parse_args()
    # round end_date to the next half hour. Example: "2024-11-11 03:03:00" will be rounded to "2024-11-11 03:30:00"
    args.end_date = args.end_date + (datetime.min - args.end_date) % timedelta(minutes=30)
    start_date = args.end_date - timedelta(days=args.interval)
    return start_date, args.end_date

def main():
    start_date, end_date = parse_args()
    date_query = {'start_date' : dt_isoformat(start_date), 'end_date' : dt_isoformat(end_date)}
    print(f'==== START QUERY FROM {start_date} TO {end_date} ====')
    # get access token
    access_token = get_access_token(oauth_url)
    data_res = get_data(generation_forecast_url, access_token, params = date_query, encode_dt_param=True)
    # flatten raw data
    processed_data = process_raw_data(data_res)
    # export to csv file
    processed_data.to_csv('updated_daily_forecast.csv', index=False)

if __name__ == '__main__':
    main()
    
    