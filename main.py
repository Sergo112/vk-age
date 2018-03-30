from datetime import datetime, date
from statistics import median, StatisticsError
import sys

import vk_api

token = ''  # <-- put your vk access token here
user = vk_api.VkApi(token=token)
user.get_api()


def age(user_id):
    try:
        friends = user.method('friends.get',
                              {'user_id': user_id, 'fields': 'bdate'})['items']
    except vk_api.exceptions.ApiError:
        print('User was deleted or banned')
        return 0
    today = datetime.today().date()
    ages = []
    for friend in friends:
            try:
                bdate = list(map(int, friend['bdate'].split('.')))
                ages.append((today - date(*reversed(bdate))).days)
            except (ValueError, TypeError, KeyError):
                continue
    if len(ages):
        return median(ages) // 365
    print('There is no data available')
    return 0


def main():
    user_id = int(input('id:'))
    n = age(user_id)
    if n:
        print('Approximately', n, 'years old')

if __name__ == '__main__':
    main()
