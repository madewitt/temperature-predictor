# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from matplotlib import pyplot as plt
import numpy as np

weather_filename = 'weatherdata.csv'
weather_file = open(weather_filename)
weather_data = weather_file.read()
weather_file.close()


# print(weather_data[:200])

# Break the weather data string into lines
lines = weather_data.split('\n')
# print(lines[:2])

# Strip of the first line as labels and the rest of the lines as
# the data values
labels = lines[0]
values = lines[1:]
n_values = len(values)

year = []
month = []
day = []
max_temp = []
j_year = 1
j_month = 2
j_day = 3
j_max_temp = 5

for i_row in range(n_values):
    split_values = values[i_row].split(',')
    if len(split_values) >= j_max_temp:
        year.append(int(split_values[j_year]))
        month.append(int(split_values[j_month]))
        day.append(int(split_values[j_day]))
        max_temp.append(float(split_values[j_max_temp]))


# start_val = 19560
# end_val = start_val+31
# print(split_values[start_val:end_val],'\n')
# print(year[start_val:end_val],'\n')
# print(month[start_val:end_val],'\n')
# print(day[start_val:end_val],'\n')
# print(max_temp[start_val:end_val],'\n')
#
# plt.scatter(range(len(max_temp)),max_temp)


# Isolate the recent data
i_mid = len(max_temp) // 2
temps = np.array(max_temp[i_mid:])
temps[np.where(temps == -99.9)] = np.nan
year = np.array(year[i_mid:])
month = np.array(month[i_mid:])
day = np.array(day[i_mid:])


# print(np.where(np.isnan(temps))[0])
# print(np.where(np.logical_not(np.isnan(temps)))[0][0])

# Start the data where the large number of consecutive nans stops
i_start = np.where(np.logical_not(np.isnan(temps)))[0][0]
temps = temps[i_start:]
year = year[i_start:]
month = month[i_start:]
day = day[i_start:]

b = np.isnan(temps)
i_nans = np.where(np.isnan(temps))[0]
# print(i_nans)

# Replace all nans with the most recent non-nan value
for i in i_nans:
    temps[i] = temps[i-1]

# print(temps[b])

# Determine whether the previous day's temperature is
# related to that of today.

# plt.plot(temps[:-1],temps[1:],color='black',marker='.',linestyle='None')
# plt.show()


# Show the relationship between two variables adding some normally
# distributed jitter
def scatter_with_jitter(x, y):
    '''
    Make a scatter plot with jitter
    '''
    x_jitter = x + np.random.normal(loc=0, scale=0.5, size=x.size)
    y_jitter = y + np.random.normal(loc=0, scale=0.5, size=y.size)
    plt.plot(
        x_jitter, y_jitter,
        color='black',
        marker='.',
        linestyle='None',
        alpha=0.1
    )
    plt.show()


# shift = 1
# scatter_with_jitter(temps[:-shift],temps[shift:])
autocorr = []
for shift in range(1, 1000):
    correlation = np.corrcoef(temps[:-shift], temps[shift:])[0, 1]
    autocorr.append(correlation)

# Add a sine wave approximation to fit autocorr for up to 1000 day shifts
d = np.arange(1000)
fit = 0.6*np.sin((2*np.pi/365)*(d+91.25))
# plt.plot(d,fit,color='green')
# plt.plot(autocorr)
# plt.show()


def find_day_of_year(year, month, day):
    """
    Convert (year,month,day) to day of the year (out of 366)
    January 1 = 0

    Parameters
    ----------
    year: int
    month: int
    day: int

    Returns
    -------
    day_of_year: int
    """

    leap_flag = year % 4 == 0
    feb_days = np.where(leap_flag, 29, 28)
    days_per_month = np.array([31, feb_days, 31, 30, 31, 30, 31, 31,
                               30, 31, 30, 31])
    return np.sum(days_per_month[0:month-1]) + day - 1


day_of_year = np.zeros(temps.size)
for i_row in range(temps.size):
    day_of_year[i_row] = find_day_of_year(
        year[i_row], month[i_row], day[i_row])

# print(year[:10])
# print(month[:10])
# print(day[:10])
# print(day_of_year[:10])

# scatter_with_jitter(day_of_year,temps)

# Create 10 day medians for each day of the year
median_temp_calendar = np.zeros(366)
ten_day_medians = np.zeros(temps.size)
for i_day in range(0, 365):
    if i_day < 5:
        begin_window_day = i_day + 365 - 5
    else:
        begin_window_day = i_day - 5
    i_begin_window = list(np.where(day_of_year == begin_window_day)[0])
    i_window_days = []
    for index in i_begin_window:
        for i in range(10):
            if index + i < temps.size:
                i_window_days.append(index + i)
    ten_day_median = np.median(temps[i_window_days])
    median_temp_calendar[i_day] = ten_day_median
    ten_day_medians[np.where(day_of_year == i_day)] = ten_day_median

    if i_day == 364:
        ten_day_medians[np.where(day_of_year == 365)] = ten_day_median
        median_temp_calendar[365] = ten_day_median

# plt.plot(np.arange(temps.size),ten_day_medians,marker='.',linestyle='None')
# plt.show()
# plt.plot(temps)
# plt.plot(median_temp_calendar)
plt.plot(ten_day_medians)
plt.show()
