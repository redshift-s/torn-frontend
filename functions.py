from unittest import result
import requests
import os
import time

from dotenv import load_dotenv

load_dotenv()

def request_data(api_type, selections, api_key, id='', comment='test', site='torn'):

    if site == 'torn' and api_type in ['user', 'faction', 'company', 'market', 'torn', 'property']:
        url = f'https://api.torn.com/{api_type}/{id}?selections={selections}&key={api_key}&comment={comment}'
    elif site == 'torn' and api_type == 'image':
        url = f'https://factiontags.torn.com/{selections}'
    elif site == 'tornstats': # and selections== 'user': or 'faction"
        url = f'https://www.tornstats.com/api/v2/{api_key}/spy/{selections}/{id}'
    else:
        url = 'gg'
    print(url)
    data = requests.get(url).json()
    #print(data)

    #https://www.tornstats.com/api/v2/{key}/spy/user/{user_id}
    #https://www.tornstats.com/api/v2/{key}/spy/faction/{faction_id}
    return data


def get_faction(id):
    response = request_data(api_type='faction', selections="" , api_key=os.environ['API_KEY'], id=id, comment='test', site='torn')
    #print(response)
    
    results = []
    faction = response["name"]
    members = response["members"]

    for member_id, member_details in members.items():
        member_name = member_details['name']
        level = member_details['level']
        last_action = member_details['last_action']['relative']
        status = member_details['last_action']['status']
        description = member_details['status']['description']
        until = epoch_to_sec(member_details['status']['until'])
        results.append({
            "faction": faction,
            "member_id": member_id,
            "member_name": member_name,
            "level": level,
            "profile": f'https://www.torn.com/profiles.php?XID={member_id}',
            "description": description,
            "status": status,
            "last_action": last_action,
            "until": until,
            'attack': f'https://www.torn.com/loader.php?sid=attack&amp;user2ID={member_id}'
        })
    
    r = request_data(api_type='faction', selections="faction" , api_key=os.environ['TS_API_KEY'], id=id, comment='test', site='tornstats')


    tornstats = []
    faction_members = r["faction"]['members']
    for member_id, member_details in faction_members.items():
        strength = member_details['spy']['strength']
        bs = member_details['spy']['total']
        tornstats.append({
            "member_id": member_id,
            "strength": int_to_b(strength),
            "bs": int_to_b(bs)
        })
        
    #print(tornstats)
    
    joined_dict = join_data(results, tornstats, "member_id")
    #print(results)

    final = joined_dict
    #print(final)
    print("run")
    sorted_data = sorted(final, key=lambda x: x['until'], reverse=False)


    return sorted_data, faction


current_time = int(time.time())

def epoch_to_sec(epoch):
    if epoch == 0:
        return 99999999
    padding = 8
    number_as_string = str(epoch - current_time)
    seconds_until = "0" * (padding - len(number_as_string)) + str(epoch - current_time)
    seconds_until = int(seconds_until)

    return seconds_until

def join_data(list1, list2, id_field):
    joined = []
    for item1 in list1:
        id_value = item1[id_field]
        for item2 in list2:
            if item2[id_field] == id_value:
                item = {**item1, **item2}
                item.pop(id_field, None)
                joined.append(item)
    return joined

def int_to_b(value):
    if value != "N/A":
        return "{:.2f}".format(value/1000000000)
    else:
        return 0

def format_number(num):
    suffix = ''
    if num >= 10**15:
        suffix = 'Q'
        num /= 10**15
    elif num >= 10**12:
        suffix = 'T'
        num /= 10**12
    elif num >= 10**9:
        suffix = 'B'
        num /= 10**9
    elif num >= 10**6:
        suffix = 'M'
        num /= 10**6
    elif num >= 10**3:
        suffix = 'k'
        num /= 10**3
    return '{:.2f}{}'.format(num, suffix)