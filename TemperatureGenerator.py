# Temperature Generator
# A proof of concept for generating fiction daily max temperatures for every day of the year
# based on mean monthly temperatures for Observatory Hill, Sydney
# from 1980 to 2010 as collated by the B.O.M.
# By Paul Maxwell-Walters, done on 02/06/2018

import random
import matplotlib
import matplotlib.pyplot as plt
import numpy as npy
import csv

months_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
months_days = [31,28,31,30,31,30,31,31,30,31,30,31]
step_value = 3

mean_monthly_temp_C_Sydney = [26.5, 26.5, 25.4, 23.3, 20.6, 18.0, 17.4, 18.9, 21.2, 22.8, 23.8, 25.5]
bound_monthly_temp_C_Sydney = [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5] # Simulated number of degrees C above and below the mean beyond which random walks are blocked
# Mean Masd Monthly Temperature for Sydney (Observatory Hill) aggregated from 1980 to 2010
# See http://www.bom.gov.au/jsp/ncc/cdio/cvg/av?p_stn_num=066062&p_prim_element_index=0&p_comp_element_index=0&redraw=null&p_display_type=statistics_summary&normals_years=1981-2010&tablesizebutt=normal

yearly_mean_temp_data = list(zip(months_names, months_days, mean_monthly_temp_C_Sydney, bound_monthly_temp_C_Sydney))
yearly_random_temp_by_month = {}

# Displays and then saves a graph of random temp data for each month to the path C:\temp\
def display_graph(month_name, days_in_month, monthly_random_temp):
    days = list(range(1, 1+days_in_month))
    plt.scatter(days, monthly_random_temp)
    plt.title("Random Walk Daily Temperature Data for Month: " + month_name)
    plt.xlabel("Day of Month")
    plt.ylabel("Maximum Temperature")
    plt_for_save = plt.gcf()
    plt.show()
    plt_for_save.savefig('\\temp\\Random_Temp_For_' + month_name + '.png')

# Saves a CSV file of all random maximum temp data per day to the path C:\temp\
def write_to_csv(month_name, days_in_month, yearly_random_temp_by_month):
    with open("\\temp\\Random_Temp_For_All Months.csv","w", newline="") as csv_file:
        days = list(range(1, 1 + days_in_month))
        field_names = ["Month"]
        field_names += days

        writer = csv.writer(csv_file)
        writer.writerow(["Month"] + days)
        for key, value in yearly_random_temp_by_month.items():
            writer.writerow([key] + value)

# Returns a simulated decimal step chNge number between -step_value and step_value
def step_change():
    return random.choice([-1*step_value,step_value])*random.random()

# For each day of the year, simulates a Monte Carlo Random Walk, bounded by the Standard Deviation
# to create a maximum temperature. Assumes a maximum change per day of 2 or 3 degrees.
# Starting point is the mean monthly temperature as in mean_monthly_temp_C_Sydney.
# A typical outcome of using a Random Walk is that the generated data has defined trends, peaks and troughs
# like normal weather, however the parameters may have to be tweaked to make them more realistic
for data_for_month in yearly_mean_temp_data:
    (month_name, days_in_month, mean_monthly_temp, bound_monthly_temp) = data_for_month
    monthly_random_temp = []
    daily_temp = mean_monthly_temp

    for i in range(1,1+days_in_month):

        # Adds the step change. If daily_temp is out of bounds then a new step change is selected. Prevents wild temperature variances.
        daily_temp += step_change()
        while (daily_temp < mean_monthly_temp - bound_monthly_temp) or (daily_temp > mean_monthly_temp + bound_monthly_temp):
            daily_temp += step_change()

        monthly_random_temp.append(daily_temp)

    display_graph(month_name, days_in_month, monthly_random_temp)
    yearly_random_temp_by_month[month_name] = monthly_random_temp

write_to_csv(month_name, days_in_month, yearly_random_temp_by_month)




