"""
A simple web scraper tool for grabbing data from weather underground's hourly data on individual
dates' pages.

"""

from __future__ import print_function
import urllib2
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta, date


def scrape_wu_page(full_url):
    page = urllib2.urlopen(full_url)
    soup = BeautifulSoup(page, 'lxml')
    hourly_table_rows = soup.find('table', class_='obs-table responsive').findAll("tr")
    columns = [entry.find(text=True) for entry in hourly_table_rows[0].findAll('th')]
    day_data_dict = dict()
    for i, row in enumerate(hourly_table_rows):
        if i > 0:
            entries = row.findAll('td')
            result_list = []
            for j, entry in enumerate(entries):
                numerical_val = entry.find("span", class_="wx-value")
                if numerical_val is None:
                    # reset back to entry
                    numerical_val = entry
                result_list.append(numerical_val.find(text=True).strip('\n').strip('\t'))
            day_data_dict[i] = result_list
    day_df = pd.DataFrame(day_data_dict).transpose()
    day_df.columns = columns
    return day_df


if __name__ == "__main__":
    # Enter date range here:
    start_date = date(2015, 6, 1)
    end_date = date(2018, 3, 1)

    # Enter desired weather station code here (note LA = 'KCQT', SF = 'KSFO'):
    weather_station = 'KSFO'


    all_weather_data = None
    day_count = (end_date - start_date).days + 1
    for single_date in (start_date + timedelta(n) for n in range(day_count)):
        print(single_date)
        full_url = "https://www.wunderground.com/history/airport/{}/{:.0f}/{:.0f}/{:.0f}/DailyHistory.html".format(
                    weather_station, single_date.year, single_date.month, single_date.day)
        day_df = scrape_wu_page(full_url)
        day_df.index = [datetime.strptime(single_date.strftime('%m%d%y ') + hours, '%m%d%y %I:%M %p') for
                        hours in day_df['Time '].values]
        if all_weather_data is None:
            all_weather_data = day_df
        else:
            all_weather_data = pd.concat([all_weather_data, day_df])
all_weather_data.to_csv(weather_station + ' weather data.csv', encoding='utf-8')
