import math
import matplotlib.pyplot as plt
from datetime import date

import datetime 
# data from Feb 29 onwards , source: wikipedia 
# n_cases = [24, 42, 57, 85, 111, 175, 252, 352, 495, 643, 932, 1203, 1598, 2160, 2827, 3497, 4372, 5656, 8054, 11980, 16668]
n_cases = {}
n_cases['Washington'] = [102, 136, 162, 267, 366, 457, 568, 642, 769, 904, 1012, 1187, 1376, 1524, 1739]
n_cases['California'] = [88, 114, 133, 157, 198, 247, 335, 392, 472, 598, 675, 1006, 1224, 1468, 1733]
n_cases['Georgia'] = [8, 12, 17, 21, 33, 41, 41, 74, 110, 122, 145, 202, 288, 482, 546, 621, 772]
n_cases['New York'] = [89, 105, 142, 173, 216, 325, 421, 613, 729, 950, 1374, 2480, 5711, 8402, 10356, 15168, 20875]
n_cases['Italy'] = [1694, 2036, 2502, 3089, 3858, 4636, 5883, 7375, 9172, 10149, 12462, 15113, 17660, 21157, 24747, 27980, 31506, 35713, 41035, 47021, 53578, 59138, 63937]
n_cases['France'] = [949, 1126, 1412, 1784, 2281, 2876, 3661, 4499, 5423, 6633, 7730, 9134, 10995, 12612, 14459, 16689, 19846]
n_cases['Germany'] = [684, 847, 1113, 1460, 1884, 2369, 3062, 3795, 4838, 6012, 7156, 8198, 10999, 13957, 16662, 18610, 22672]

update_date = {}
update_date['Washington'] = datetime.date(2020,3,22)
update_date['New York'] = datetime.date(2020,3,23)
update_date['California'] = datetime.date(2020,3,22)
update_date['Georgia'] = datetime.date(2020,3, 23)
update_date['Italy'] = datetime.date(2020,3, 23)
update_date['France'] = datetime.date(2020,3, 23)
update_date['Germany'] = datetime.date(2020, 3, 23)


# update_date['California']

def get_dates_labels(offset=0, tick_horizon=2, days_range=None):
    # labeling start date = start_date + offset THIS CAN BE USED FOR GEORGIA DATA ONLY
    # tick_horizon = 2
    start_date = datetime.date(2020,3,7)
    time_delta = datetime.timedelta(days=tick_horizon)
    date_format = lambda date_obj: "{:}-{:}".format(date_obj.month, date_obj.day)
    if days_range is None:
        start_tick = 0
        end_tick = int((date.today() - start_date).days) - offset
    else:
        start_tick, end_tick = days_range

    date_ticks = []
    cur_date = start_date + datetime.timedelta(days=offset + start_tick)
    all_dates = []
    for i in range(start_tick, end_tick, tick_horizon):
        date_ticks.append(i)
        all_dates.append(date_format(cur_date))
        cur_date += time_delta
    return (date_ticks, all_dates)

def cut_data(data, start_date, update_date=date.today(), offset=0):
    """cur data from start_date to today inclusive of end points"""
    n = (update_date - start_date).days + 1 + offset
    return data[-n:]



def compute_moving_avg(n_cases, horizon=3):
    # let l = len(n_cases), return a l-horizon  vector of average growth rate
    average_growth_rates = []
    for i in range(horizon, len(n_cases)):
        start = i - horizon
        end = i
        ratio = n_cases[end] / float(n_cases[start])
        growth_rate = math.exp(math.log(ratio) / float(horizon))
        average_growth_rates.append(growth_rate)
    return average_growth_rates





## analyze the moving average from a fixed date, as trigger event to see the effectiveness of measures 
closing_schools = {}
closing_schools['Washington'] = datetime.date(2020,3,12)
closing_schools['New York'] = datetime.date(2020,3,13)
closing_schools['California'] = datetime.date(2020,3,13)
closing_schools['Georgia'] = datetime.date(2020,3,13)
closing_schools['Italy'] = datetime.date(2020,3,4)
closing_schools['France'] = datetime.date(2020,3,13)
closing_schools['Germany'] = datetime.date(2020, 3, 13)
# closing_schools['SK'] = datetime.date()

plt.figure()
plt.title('average growth rate since school closure')
offset=4
for state in n_cases.keys():
    data = cut_data(n_cases[state], closing_schools[state], update_date=update_date[state], offset=offset)
    moving_avg = compute_moving_avg(data, horizon=5)
    plt.plot(moving_avg, label=state)
    plt.xlabel('days')
    plt.ylabel('growth_rate')
    plt.axvline(x=offset)
plt.legend()
plt.savefig('closign_schools')


###### analysis for Georgia

g_cases = n_cases['Georgia']
for moving_ave_horizon in [3,5]:

    plt.figure()
    plt.subplot(211)
    plt.plot(g_cases)
    date_ticks, all_dates = get_dates_labels()
    plt.xticks(date_ticks, all_dates)
    plt.yscale('log')
    plt.ylabel('Num Cases')
    plt.title(" Average Rate, Horizon {:}, Data Source: Wikipedia Covid USA".format(moving_ave_horizon))

    date_ticks, all_dates = get_dates_labels(offset=moving_ave_horizon)
    average_growth_rates = compute_moving_avg(g_cases, horizon=moving_ave_horizon)


    plt.subplot(212)
    target = 5000

    plt.plot(average_growth_rates)

    plt.xticks(date_ticks, all_dates)
    plt.ylabel('ave_growth_rate')
    plt.savefig('./Georgia/ {:} {:} rate moving_ave length  '.format(date.today(), moving_ave_horizon))
    plt.figure()
    
    plt.subplot(211)
    plt.title('Time to Amegaden Date, AKA {:}k cases'.format(target/1000))
    number_days_to_blow_up = [math.log(target / float(g_cases[moving_ave_horizon + idx])) / math.log(ele) for (idx, ele) in enumerate(average_growth_rates)]
    plt.plot(number_days_to_blow_up)

    # plt.plot(average_growth_rates)

    plt.xticks(date_ticks, all_dates)
    plt.ylabel('days to {:}k cases'.format(target/1000))
    # plt.show()
    

    # plt.figure()
    plt.subplot(212)
    int_number_days = [int(ele) + idx for (idx, ele) in enumerate(number_days_to_blow_up)]
    y_tick, y_label = get_dates_labels(offset=moving_ave_horizon, tick_horizon=1, days_range=[min(int_number_days), max(int_number_days)])
    plt.plot(int_number_days)
    plt.xticks(date_ticks, all_dates)
    plt.yticks(y_tick, y_label)
        # plt.show()
    plt.savefig('./Georgia/ {:} {:} amegaden date move_ave length 1'.format(date.today(), moving_ave_horizon))
