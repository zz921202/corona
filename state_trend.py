from log_trend import * 
###### analysis for Georgia

start_date = {}
record_state = {'USA', 'Georgia'}
start_date['USA'] = datetime.date(2020, 2, 29)
start_date['Georgia'] = datetime.date(2020, 3, 7)


def get_dates_labels(offset=0, tick_horizon=2, days_range=None, start_date=datetime.date(2020,3,7),end_date=date.today()):
    # labeling start date = start_date + offset THIS CAN BE USED FOR GEORGIA DATA ONLY
    # tick_horizon = 2
    # start_date = datetime.date(2020,3,7)
    time_delta = datetime.timedelta(days=tick_horizon)
    date_format = lambda date_obj: "{:}-{:}".format(date_obj.month, date_obj.day)
    if days_range is None:
        start_tick = 0
        end_tick = int((end_date - start_date).days) - offset
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

def get_start_date(data_lis, update_date=date.today()):
    return update_date - datetime.timedelta(days=len(data_lis) - 1)


states = ['Georgia', 'USA', 'New York', 'California', 'Washington']

start_date = min([get_start_date(n_cases[state], update_date=update_date[state]) for state in states])
end_date = max([update_date[state] for state in states])
xlim = [0, (end_date - start_date).days]
date_ranges = {}
for state in states:
    offset = (get_start_date(n_cases[state], update_date=update_date[state]) - start_date).days 
    date_ranges[state] = range(offset, offset + len(n_cases[state]) )

for moving_ave_horizon in [3,5]:

    plt.figure()
    plt.subplot(211)
    for state in states:
        plt.plot(date_ranges[state], n_cases[state], label=state)
    date_ticks, all_dates = get_dates_labels(start_date=start_date)
    plt.xticks(date_ticks, all_dates)
    plt.yscale('log')
    plt.ylabel('Num Cases')
    plt.legend()
    plt.title(" Average Rate, Horizon {:}, Data Source: Wikipedia Covid USA".format(moving_ave_horizon))

    # date_ticks, all_dates = get_dates_labels(offset=moving_ave_horizon)

    


    plt.subplot(212)
    for state in states:
        average_growth_rates = compute_moving_avg(n_cases[state], horizon=moving_ave_horizon)
        plt.plot(date_ranges[state][moving_ave_horizon:], average_growth_rates, label=state)
        plt.xlim = xlim

    plt.xticks(date_ticks, all_dates)
    plt.legend()
    plt.ylabel('ave_growth_rate')
    # plt.savefig('./Georgia/ {:} {:} rate moving_ave length  '.format(date.today(), moving_ave_horizon))

    plt.figure()
    target = 5000
    g_cases = n_cases['Georgia']
    average_growth_rates = compute_moving_avg(g_cases, horizon=moving_ave_horizon)

    plt.subplot(211)
    plt.title('Time to Amegaden Date, AKA {:}k cases'.format(target/1000))
    number_days_to_blow_up = [math.log(target / float(g_cases[moving_ave_horizon + idx])) / math.log(ele) for (idx, ele) in enumerate(average_growth_rates)]
    plt.plot(number_days_to_blow_up)

    # plt.plot(average_growth_rates)
    date_ticks, all_dates = get_dates_labels(offset=moving_ave_horizon, end_date=update_date['Georgia'])
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
    plt.show()
    # plt.savefig('./Georgia/ {:} {:} amegaden date move_ave length 1'.format(date.today(), moving_ave_horizon))
