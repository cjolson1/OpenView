from pandas import read_csv
import datetime
import random

data_frame = read_csv('static/BDeer_VMWorld_2017.csv')

def get_data(type, start, end):
    start_date = datetime.datetime.strptime(start, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end, '%Y-%m-%d')
    def in_range(date):
        try:
            return start_date <= datetime.datetime.strptime(date, '%Y-%m-%d') <= end_date
        except:
            try:
                return start_date <= datetime.datetime.strptime(date, '%b %d %Y') <= end_date
            except:
                return False
    def get_date_val(date):
        try:
            date = datetime.datetime.strptime(date, '%b %d %Y')
            year = date.year
            month = date.month
            day = date.day
            return year + 1.0/12*month + 1.0/365*day
        except:
            try:
                date = datetime.datetime.strptime(date, '%Y-%m-%d')
                year = date.year
                month = date.month
                day = date.day
                return year + 1.0 / 12 * month + 1.0 / 365 * day
            except:
                return 0
    ret = {
        type: {
            'data': None,
            'layout': None,
            'note': None
        }
    }
    data_set = list(set(data_frame[type]))
    if type == 'details.total_money_in_usd':
        data = []
        max_money = 0
        min_money = 61651651684654654
        for i, money in enumerate(data_frame[type]):
            if money != 'Undisclosed' and in_range(data_frame['founded_date'][i]) and get_date_val(data_frame['founded_date'][i]):
                    date_val = get_date_val(data_frame['founded_date'][i])
                    money_val = float(money[1:len(money) - 1])
                    if money_val > max_money:
                        max_money = money_val
                    elif money_val < min_money:
                        min_money = money_val
                    name = data_frame['name'][i]
                    trace = {
                        'x': [date_val],
                        'y': [money_val],
                        'mode': 'markers',
                        'type': 'scatter',
                        'name': name,
                        'marker': {
                            'size': 8
                        }
                    }
                    data.append(trace)
        layout = {
            'xaxis': {
                range: [.8*get_date_val(start_date), 1.2*get_date_val(end_date)]
            },
            'yaxis': {
                range: [.5*min_money, 1.25*max_money]
            },
            'title': 'Data Labels Hover'
        }
        note = '* Does not include Undisclosed Funding Data.'
    elif type == 'tier':
        values = [0]*len(data_set)
        counter = 0
        for i, entry in enumerate(data_frame[type]):
            if in_range(data_frame['sf_last_activity_date'][i]):
                try:
                    values[data_set.index(entry)] += 1
                    counter += 1
                except (ValueError, IndexError):
                    continue
        for i in range(len(values)):
            values[i] = values[i]/float(counter)
        data = [{
            'values': values[:],
            'labels': data_set,
            'type': 'pie'
        }]
        layout = {
            'height': 400,
            'width': 500
        }
        note = '* Does not include companies who have no last activity date.'
    elif type == 'status':
        values = [0] * len(data_set)
        counter = 0
        for i, entry in enumerate(data_frame[type]):
            if in_range(data_frame['sf_last_activity_date'][i]):
                try:
                    values[data_set.index(entry)] += 1
                    counter += 1
                except (ValueError, IndexError):
                    continue
        for i in range(len(values)):
            values[i] = values[i] / float(counter)
        data = [{
            'values': values[:],
            'labels': data_set,
            'type': 'pie'
        }]
        layout = {
            'height': 400,
            'width': 500
        }
        note = '* Does not include companies who have no last activity date.'
    elif type == 'sf_account_owner':
        account_owner_col = list(data_frame['sf_account_owner'])
        activity_x = [0]*len(data_set)
        r = lambda: random.randint(0, 255)
        color = 'rbga({0},{1},{2})'.format(r(), r(), r())
        activity = {
            'x': activity_x,
            'y': data_set,
            'name': 'Activity',
            'orientation': 'h',
            'marker': {
                'color': color,
                'width': 1
            },
            'type': 'bar'
        }
        color = 'rbga({0},{1},{2})'.format(r(), r(), r())
        no_activity_x = [0]*len(data_set)
        no_activity = {
            'x': no_activity_x,
            'y': data_set,
            'name': 'No activity',
            'orientation': 'h',
            'marker': {
                'color': color,
                'width': 1
            },
            'type': 'bar'
        }
        for name in data_set:
            for i, date in enumerate(list(data_frame['sf_last_activity_date'])):
                if in_range(date) and account_owner_col[i] == name:
                    activity_x[data_set.index(name)] += 1
                elif date == 'No activity':
                    no_activity_x[data_set.index(name)] += 1
        data = [activity, no_activity]
        layout = {
            'title': 'Account Owner vs. Last Activity Date from {0} to {1}'.format(start_date, end_date),
            'barmode': 'stack'
        }
        note = ''




    ret[type]['data'], ret[type]['layout'], ret[type]['note'] = data, layout, note

get_data('details.total_money_in_usd', '1999-05-09', '2016-12-23')

