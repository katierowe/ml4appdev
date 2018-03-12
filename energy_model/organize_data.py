'''
Parses data files containing energy demand data retrieved from:
https://www.eia.gov/realtime_grid/

And hourly weather data from:
http://ipm.ucanr.edu/WEATHER/



'''
import pandas as pd
import numpy as np
import math
import os


def compile_energy_data(directory):
    column_dict = {'BA': 'balancing_authority',
                   'VAL_D': 'demand',
                   'VAL_DF': 'demand_forecast',
                   'VAL_NG': 'net_generation',
                   'VAL_TI': 'total_interchange',
                   'LOCAL_HOUR_INT': 'hour_of_day'}
    total_df = None
    for file in os.listdir(directory):
        df = pd.read_csv(directory + '/' + file, index_col='LOCAL_TIMESTAMP', parse_dates=True)
        if total_df is None:
            total_df = df
        else:
            total_df = total_df.append(df)
    total_df.columns = [column_dict[c] if c in column_dict.keys() else c for c in total_df.columns]
    total_df['LOCAL_DATE'] = pd.to_datetime(total_df['LOCAL_DATE'])
    total_df['day_of_week'] = total_df.index.weekday
    total_df['weekday'] = total_df['day_of_week'] < 5
    total_df['month'] = total_df.index.month
    total_df['day_of_month'] = total_df.index.day
    total_df['year'] = total_df.index.year
    #print total_df['hour_of_day'].values
    #print math.pi * total_df['hour_of_day'].values
    #print 2. * math.pi * total_df['hour_of_day'].values / 24.
    total_df['hour_sin'] = np.sin((2. * math.pi * total_df['hour_of_day'].values / 24.))
    total_df['hour_cos'] = np.cos((2. * math.pi * total_df['hour_of_day'].values / 24.))
    total_df['month_sin'] = np.sin((2. * math.pi * total_df['month'].values / 12.))
    total_df['month_cos'] = np.cos((2. * math.pi * total_df['month'].values / 12.))
    total_df['day_of_week_sin'] = np.sin((2. * math.pi * total_df['day_of_week'].values / 7.))
    total_df['day_of_week_cos'] = np.cos((2. * math.pi * total_df['day_of_week'].values / 7.))
    ciso = total_df[total_df['balancing_authority'] == 'CISO']
    ciso = ciso[~ciso.index.duplicated(keep='first')]
    ciso.to_csv('CISO_data.csv')
    return ciso

def add_prev_time_features(ciso):
    index_timestamps = ciso.index
    ciso.loc[:, 'previous_day_demand'] = float('NaN')
    ciso.loc[:, 'previous_week_demand'] = float('NaN')
    demand = ciso['demand']
    for index, row in ciso.iterrows():
        start_of_day = index.floor(pd.Timedelta('1 day'))
        prev_week = start_of_day - pd.Timedelta('7 day')
        ciso.loc[index, 'previous_week_demand'] = demand[(demand.index < start_of_day) &
                                                         (demand.index >= prev_week)].mean()

        prev_time = index - pd.Timedelta('1 day')
        if prev_time in index_timestamps:
            try:
                ciso.loc[index, 'previous_day_demand'] = demand.loc[prev_time]
            except ValueError:
                print ciso.loc[prev_time, 'demand']
                print ciso.loc[index, 'previous_day_demand']

    ciso = ciso.dropna(subset=['previous_day_demand'])
    return ciso

def add_weather_data(directory, data):
    #weather = pd.read_csv(open(directory + '/lodi_weather2.csv', 'rU'), engine='python')
    code_dict = {'KSFO': 'SF', 'KCQT': 'LA'}
    for code in code_dict.keys():
        print code
        weather = pd.read_csv('{}/{} weather data.csv'.format(directory, code), index_col=0, parse_dates=True)
        weather = weather[~weather.index.duplicated()].sort_index()
        temperature = pd.to_numeric(weather['Temp.'].reindex(data.index, method='nearest'), errors='coerce')
        temperature = temperature.interpolate(method='time')
        data[code_dict[code] + ' temp'] = temperature
    return data

def add_price_data(directory, data):
    '''
    Adds data from files obtained from:
    https://www.eia.gov/electricity/wholesale/#history

    :param directory:
    :param data:
    :return:
    '''
    price_dict = {'ERCOT': ['ERCOT North 345KV Peak'], 'MISO': ['Indiana Hub RT Peak'],
                  'Northwest': ['Mid C Peak'], 'CISO': ['NP15 EZ Gen DA LMP Peak', 'SP15 EZ Gen DA LMP Peak'],
                  'ISONE': ['Nepool MH DA LMP Peak'], 'PJM': ['PJM WH Real Time Peak'],
                  'Southwest':['Palo Verde Peak']}
    prices = None
    for file in os.listdir(directory):
        yearly_prices = pd.read_excel(directory + '/' + file)
        if prices is None:
            prices = yearly_prices
        else:
            prices = pd.concat([prices, yearly_prices])
    for price_hub in price_dict['CISO']:
        data[price_hub + ' wtd avg'] = float('NaN')
        data[price_hub + ' change'] = float('NaN')
        ciso_prices = prices[prices['Price hub'] == price_hub]
        ciso_prices.index = pd.to_datetime(ciso_prices['Delivery start date'])
        for timestamp in data.index:
            date = timestamp.date()
            if date in ciso_prices.index:
                try:
                    data.loc[timestamp, price_hub + ' wtd avg'] = ciso_prices.loc[date, 'Wtd avg price $/MWh']
                    data.loc[timestamp, price_hub + ' change'] = ciso_prices.loc[date, 'Change']
                except ValueError:
                    print 'Could not find prices at: ', timestamp, date
        # forward-fill na values to cover weekends where no price info was available.
        data.loc[:, price_hub + ' wtd avg'] = data.loc[:, price_hub + ' wtd avg'].fillna(method='ffill')
        data.loc[:, price_hub + ' change'] = data.loc[:, price_hub + ' change'].fillna(0)
    return data




if __name__ == "__main__":
    root_directory = os.path.expanduser('~/energy_app_data')
    #ciso = compile_energy_data(root_directory + '/energy')
    ciso = pd.read_csv('CISO_data.csv', index_col=0, parse_dates=True)
    #ciso = add_prev_time_features(ciso)
    #ciso = add_weather_data(root_directory + '/weather', ciso)
    ciso = add_price_data(root_directory + '/pricing', ciso)
    #print ciso
    ciso.to_csv('CISO_data.csv')
