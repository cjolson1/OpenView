from pandas import read_csv
import datetime
import random

data_frame = read_csv('static/BDeer_VMWorld_2017.csv')
pass_data_frame = read_csv('static/passed.csv')

average_vals = {
    'tier_avg': 0,
    'lfaa': 0,
    'tfaa': 0,
    'employee_avg': 0,
    'delta_avg': 0,
    'founded_avg': 0
}

tier_value = {
    'Pass': 3,
    'No Tier': 0,
    'Tier 1': 2,
    'Tier 0': 1,
    'General': 0
}

def get_date_val(date):
    try:
        date = datetime.datetime.strptime(date, '%b %d %Y')
        year = date.year
        month = date.month
        day = date.day
        return year + 1.0 / 12 * month + 1.0 / 365 * day
    except:
        try:
            date = datetime.datetime.strptime(date, '%Y-%m-%d')
            year = date.year
            month = date.month
            day = date.day
            return year + 1.0 / 12 * month + 1.0 / 365 * day
        except:
            return 0


def get_average_data(file):
    ret = {}
    tier_average = 0
    tier_counter = 0
    for tier in file['tier']:
        try:
            tier_average += tier_value[tier]
            tier_counter += 1
        except KeyError:
            continue
    tier_average /= float(tier_counter)
    ret['tier_avg'] = tier_average

    last_funding_amount_average = 0
    lfaa_counter = 0
    for lfa in file['details.last_funding_amount']:
        try:
            amount = float(lfa[1:len(lfa)-1])
            lfaa_counter += 1
            last_funding_amount_average += amount
        except ValueError:
            continue
    last_funding_amount_average /= float(lfaa_counter)
    ret['lfaa'] = last_funding_amount_average

    total_funding_amount_average = 0
    tfaa_counter = 0
    for tfa in file['details.total_money_in_usd']:
        try:
            amount = float(tfa[1:len(tfa)-1])
            tfaa_counter += 1
            total_funding_amount_average += amount
        except ValueError:
            continue
    total_funding_amount_average /= float(tfaa_counter)
    ret['tfaa'] = total_funding_amount_average

    num_employees_average = 0
    employee_counter = 0
    for employee in file['employee_data.num_employees']:
        try:
            num_employees_average += int(employee)
            employee_counter += 1
        except:
            continue
    num_employees_average /= (float(employee_counter)*1000)
    ret['employee_avg'] = num_employees_average

    delta_employees_average = 0
    delta_counter = 0
    for delta in file['employee_data.delta_num_employees_percent']:
        try:
            if int(delta) < 1000:
                delta_employees_average += float(delta)
                delta_counter += 1
        except ValueError:
            continue
    delta_employees_average /= (float(delta_counter))
    ret['delta_avg'] = delta_employees_average

    founded_average = 0
    founded_counter = 0
    for found_date in file['founded_date']:
        try:
            val = get_date_val(found_date)
            if val > 1980:
                founded_average += get_date_val(found_date)
                founded_counter += 1
        except:
            continue
    founded_average /= (float(founded_counter)*1000)
    ret['founded_avg'] = founded_average

    for key in ret:
        assert key in average_vals
        average_vals[key] += ret[key]*len(file['id'])
    return True

get_average_data(data_frame)
get_average_data(pass_data_frame)
for value in average_vals:
    average_vals[value] /= float(len(data_frame['id']) + len(pass_data_frame['id']))


def get_category_data(type, start, end):
    start_date = datetime.datetime.strptime(start, '%m/%d/%Y')
    end_date = datetime.datetime.strptime(end, '%m/%d/%Y')
    def in_range(date):
        try:
            return start_date <= datetime.datetime.strptime(date, '%Y-%m-%d') <= end_date
        except:
            try:
                return start_date <= datetime.datetime.strptime(date, '%b %d %Y') <= end_date
            except:
                return False

    ret = {
        'data': None,
        'layout': None,
        'note': None
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
            'title': 'Revenue Generated vs. Founding Date',
            'showlegend': False,
            'xaxis': {
                'title': 'Founded Date (Year)',
                'titlefont': {
                    'family': 'Courier New, monospace',
                    'size': 18,
                    'color': '#7f7f7f'
                }
            },
            'yaxis': {
                'title': 'Revenue raised (millions in USD)',
                'titlefont': {
                    'family': 'Courier New, monospace',
                    'size': 18,
                    'color': '#7f7f7f'
                }
            },
            'height': 800,
            'width': '100%'
        }
        note = '* Does not include Undisclosed Funding Data.'
    elif type == 'tier':
        values = [0]*len(data_set)
        for i, entry in enumerate(data_frame[type]):
            if in_range(data_frame['sf_last_activity_date'][i]):
                try:
                    values[data_set.index(entry)] += 1
                except (ValueError, IndexError):
                    continue
        data = [{
            'values': values[:],
            'labels': data_set,
            'type': 'pie',
            'hoverinfo': 'label+value'
        }]
        layout = {
            'height': 800,
            'width': '100%'
        }
        note = '* Does not include companies who have no last activity date.'
    elif type == 'status':
        values = [0] * len(data_set)
        for i, entry in enumerate(data_frame[type]):
            if in_range(data_frame['sf_last_activity_date'][i]):
                try:
                    values[data_set.index(entry)] += 1
                except (ValueError, IndexError):
                    continue
        data = [{
            'values': values[:],
            'labels': data_set,
            'type': 'pie',
            'hoverinfo': 'label+value'
        }]
        layout = {
            'height': 800,
            'width': '100%'
        }
        note = '* Does not include companies who have no last activity date.'
    elif type == 'sf_account_owner':
        data_set.remove('Inactive User')
        data_set.remove('Admin Oblytics')
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
                elif date == 'No activity' and account_owner_col[i] == name:
                    no_activity_x[data_set.index(name)] += 1
        data = [activity, no_activity]
        layout = {
            'title': 'Account Owner vs. Last Activity Date from {0} to {1}'.format(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')),
            'barmode': 'stack',
            'height': 800,
            'width': '100%',
            'margin': {
                'l':200
            }
        }
        note = ''
    ret['data'], ret['layout'], ret['note'] = data, layout, note
    return ret

def get_company_data(id):
    if int(id) in [int(i) for i in data_frame['id']]:
        file = data_frame
    else:
        file = pass_data_frame
    row = [int(i) for i in file['id']].index(int(id))
    try:
        tier_val = tier_value[file['tier'][row]]
    except:
        tier_val = 0
    try:
        founded_val = get_date_val(file['founded_date'][row])/float(1000)
    except:
        founded_val = 0
    try:
        lfaa = file['details.last_funding_amount'][row][1:len(file['details.last_funding_amount'][row])-1]
    except:
        lfaa = 0
    try:
        total = file['details.total_money_in_usd'][row][1:len(file['details.total_money_in_usd'][row])-1]
    except:
        total = 0
    try:
        employees = int(file['employee_data.num_employees'][row])/float(1000)
    except:
        employees = 0
    try:
        delta = float(file['employee_data.delta_num_employees_percent'][row]) if int(file['employee_data.delta_num_employees_percent'][row]) else 0
    except:
        delta = 0
    keys = list(average_vals.keys())
    old_keys = keys[:]
    names = {
        'delta_avg': 'Change in Employees (%)',
        'tfaa': 'Total Funding Received',
        'tier_avg': 'Tier Achieved',
        'employee_avg': 'Number of Employees (Thousands)',
        'lfaa': 'Last Funding Amount',
        'founded_avg': 'Founded Year (Thousands)'
    }
    labels = [average_vals[key] for key in keys]
    for i in range(len(keys)):
        keys[i] = names[keys[i]]
    average_trace = {
        'x': keys,
        'y': labels,
        'name': 'Average Across all Companies',
        'type': 'bar'
    }
    values = {
        'delta_avg': delta,
        'tfaa': total,
        'tier_avg': tier_val,
        'employee_avg': employees,
        'lfaa': lfaa,
        'founded_avg': founded_val
    }
    y = []
    for key in old_keys:
        y.append(values[key])
    trace = {
        'x': keys,
        'y': y,
        'name': file['name'][row],
        'type': 'bar'
    }
    data = [trace, average_trace]
    layout = {'barmode': 'group'}
    return {'data': data, 'layout': layout, 'note': 'Undisclosed amounts show up as None'}

