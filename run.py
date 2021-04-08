import datetime
import re
from DingTalk import *
from Config import *


# 查看硬盘空间
def check_disk(mounted_on='/'):
    cmd = "df -h"
    f = os.popen(cmd)
    for line in f.readlines():
        line = line.replace("\n", "")
        line = re.sub(' +', ' ', line)
        if line != '':
            res = line.split(' ')
            if res[5] == mounted_on:
                return res
    return False


# 查看进程运行情况
def check_process(process_name):
    cmd = "ps -ef | grep {} | grep -v grep".format(process_name)
    f = os.popen(cmd)
    arr = [x for x in f.read().split("\n") if x != '']
    return arr


# 查看队列运行情况
def check_job(password):
    cmd = "echo {} | sudo -S supervisorctl status".format(password)
    f = os.popen(cmd)
    jobs = [re.sub(' +', ' ', x) for x in f.read().split("\n") if x != '']
    res = {}
    for job in jobs:
        arr = job.split(" ")
        key = arr[0]
        if ":" in arr[0]:
            key = arr[0].split(":")[0]
        if key not in res.keys():
            res[key] = arr[1]
    return res


if __name__ == '__main__':
    # 配置
    config_ding = Config.params['ding']
    config_alarm = Config.params['alarm']
    config_system = Config.params['system']
    config_process = Config.params['process']

    disk_mounted_on = config_alarm['disk-mounted-on']
    ding_mobiles = config_alarm['mobiles'].split(',')

    mobile_text = "".join(["@{}".format(x) for x in ding_mobiles])
    # 钉钉
    ding = DingTalk(config_ding['url'], config_ding['secret'])

    if ',' in disk_mounted_on:
        disks = disk_mounted_on.split(',')
    else:
        disks = [disk_mounted_on]

    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if Config.params['debug']:
        print("运行时间：", now_time)
    for disk in disks:
        disk_info = check_disk(disk)
        # ['/dev/vda1', '40G', '25G', '13G', '66%', '/']
        # 磁盘空间占用大于90%
        if disk_info and disk_info[4].replace("%", "") > config_alarm['disk-usage']:
            title = "磁盘空间不足"
            text_disk = "### 磁盘空间不足\n- 路径 {}\n- 总空间 {}\n- 已使用 {}\n- 剩余可用 {}\n- 已用占比 {}\n### 时间：{}\n{}\n".format(
                disk,
                disk_info[1],
                disk_info[2],
                disk_info[3],
                disk_info[4],
                now_time,
                mobile_text
            )
            print(text_disk)
            ding.send_markdown(title, text_disk, ding_mobiles)

    # 查看进程运行情况
    for process, process_text in config_process.items():
        if len(check_process(process_text)) < 1:
            title = '进程运行异常'
            text_process = "### 进程运行异常\n- 进程：{}\n### 时间：{}\n{}\n".format(
                process,
                now_time,
                mobile_text
            )
            print(text_process)
            ding.send_markdown(title, text_process, ding_mobiles)

    # 查看队列运行情况
    for job, status in check_job(config_system['sudo-password']).items():
        if status != 'RUNNING':
            title = '队列运行异常'
            text_job = "### 队列运行异常\n- 队列：{}\n- 当前状态：{}\n### 时间：{}\n{}\n".format(
                job,
                status,
                now_time,
                mobile_text
            )
            print(text_job)
            ding.send_markdown(title, text_job, ding_mobiles)
