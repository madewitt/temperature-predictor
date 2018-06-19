# -*- coding: utf-8 -*-
"""
A simple temperature predictor for Fort Lauderdale Florida.
"""
from matplotlib import pyplot as plt
import numpy as np

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


# Import data from the csv file
weather_filename = 'weatherdata.csv'
weather_file = open(weather_filename)
weather_data = weather_file.read()
weather_file.close()

# Break the weather data string into lines
lines = weather_data.split('\n')

# Store the first line as labels and the rest of the lines as
# the data values
labels = lines[0]
values = lines[1:]
n_values = len(values)

# Initialize lists for each relevant data field.
year = []
month = []
day = []
max_temp = []

# Define index variables for each data column in 'values'.
j_year = 1
j_month = 2
j_day = 3
j_max_temp = 5

# Split up data values using a comma delimiter and store each value
# in its corresponding list.
for i_row in range(n_values):
    split_values = values[i_row].split(',')
    if len(split_values) >= j_max_temp:
        year.append(int(split_values[j_year]))
        month.append(int(split_values[j_month]))
        day.append(int(split_values[j_day]))
        max_temp.append(float(split_values[j_max_temp]))


# Since there is a significant amount of missing data early on in the
# dataset, select out only the recent half of the data.
i_mid = len(max_temp) // 2
temps = np.array(max_temp[i_mid:])
year = np.array(year[i_mid:])
month = np.array(month[i_mid:])
day = np.array(day[i_mid:])
# Replace Florida State University's missing data temperature value of
# -99.9 with nan
temps[np.where(temps == -99.9)] = np.nan


# There is still a large number of nans in the temperature field. Eliminate
# these from the dataset.
# Find the first index after the large number of consecutive nans.
i_start = np.where(np.logical_not(np.isnan(temps)))[0][0]

# Slice the data starting at the first non-nan temperature index.
temps = temps[i_start:]
year = year[i_start:]
month = month[i_start:]
day = day[i_start:]


# Get the indices of the remaining nan values in the temperature array.
i_nans = np.where(np.isnan(temps))[0]

# Replace all remaining sparse nans in the temperature array with the
# temperature for the preceeding day.
for i in i_nans:
    temps[i] = temps[i-1]


day_of_year = np.zeros(temps.size)
for i_row in range(temps.size):
    day_of_year[i_row] = find_day_of_year(
        year[i_row], month[i_row], day[i_row])


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
