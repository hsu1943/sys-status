import collections
import datetime
import os
import time
from typing import Dict
import diskcache

cache_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'runtime')
cache = diskcache.Cache(cache_path)
# print("\n缓存路径：")
# print(cache.directory)


def get_gap_key(gap):
    if isinstance(gap, int):
        return 'sys_status_{}'.format(str(gap))
    return False


def get_gap_time_key(gap: int, time_string: str):
    # 15 分钟
    if gap == 15 * 60:
        return time_string[:-3] + ':00'
    # 1 小时
    elif gap == 60 * 60:
        return time_string[:-6] + ':00:00'
    # 一天
    elif gap == 24 * 60 * 60:
        return time_string[:-8] + '00:00:00'

    return False


# 根据条数获取所有的key
def get_gap_time_keys(gap, limit):
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # 找到最近的前一个时间点
    last_time_spot = ''
    if gap == 15 * 60:
        minutes = int(now_time[14:16])
        if minutes == 0:
            # 上一个小时的45分
            last_time_spot = (datetime.datetime.now() + datetime.timedelta(hours=-1)).strftime('%Y-%m-%d %H:45:%S')
        elif 0 < minutes <= 15:
            last_time_spot = now_time[:-6] + ':00:00'
        elif 15 < minutes <= 30:
            last_time_spot = now_time[:-6] + ':15:00'
        elif 30 < minutes <= 45:
            last_time_spot = now_time[:-6] + ':30:00'
        else:
            last_time_spot = now_time[:-6] + ':45:00'
    elif gap == 60 * 60:
        last_time_spot = now_time[:-6] + ':00:00'
    elif gap == 24 * 60 * 60:
        last_time_spot = now_time[:-8] + '00:00:00'
    time_keys = []
    for i in range(limit):
        time_array = time.strptime(last_time_spot, '%Y-%m-%d %H:%M:%S')
        timestamp = int(time.mktime(time_array)) - i * gap
        time_keys.append(datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'))

    return time_keys


def get_expire(key: str):
    fifteen_minutes_key = 'sys_status_fifteen_minutes'
    hours_key = 'sys_status_hours'
    days_key = 'sys_status_days'
    expire = 0
    if key == fifteen_minutes_key:
        expire = 180 * 3600
    elif key == hours_key:
        expire = 720 * 3600
    elif key == days_key:
        expire = 720 * 24 * 3600

    return expire


def handler(gap: int, data: Dict):
    """
    确定时间key 缓存key
    :param gap:
    :param data:
    :return:
    """
    gap_key = get_gap_key(gap)
    gap_time_key = get_gap_time_key(gap, data['time'])
    # print("\n待存储的时间段key：")
    # print(gap_key)
    # print("\n待存储的time_key：")
    # print(gap_time_key)
    # print("\n待存储的数据：")
    # print(data)
    add_one(gap_key, gap_time_key, data)


def add_one(key: str, time_key: str, value: Dict):
    """
    向缓存中添加数据
    :param key: 缓存key
    :param time_key: 单条时间key
    :param value: 单条值
    :return:
    """

    data = cache.get(key)
    if data is None:
        data = collections.OrderedDict()
    data[time_key] = value

    data = delete_expire_data(data)
    # print("\n存入前的全部数据：")
    # print(data)
    # print("\n存入数据结果：")
    cache.set(key, data)


def delete_expire_data(data: collections.OrderedDict):
    """
    缓存总条目保存 720 条 时间跨度不一样，写到不同的缓存
    :param data: 数据
    :return:
    """
    if len(data) > 720:
        print("删除一个第一个")
        data.popitem(last=False)
    return data


def get_data(gap: int, limit: int):
    # 获取当前时间之前的所有时间
    time_keys = get_gap_time_keys(gap, limit)
    # print("\n全部待取的time_key：")
    # print(time_keys)
    key = get_gap_key(gap)
    # print("\n待取时间段key：")
    # print(key)
    all_data = cache.get(key)
    # print("\n待取时间段全部缓存数据：")
    # print(all_data)
    data_list = []
    for time_key in time_keys:
        if all_data is not None and time_key in all_data.keys():
            # print("\n找到一个数据：", time_key)
            data_list.append(all_data[time_key])
    # print("\nget_data 获取到数据：")
    # print(data_list)
    return data_list
