from configparser import RawConfigParser
import os


class Config(object):
    conf = RawConfigParser()
    path = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(path, 'config.ini')
    conf.read(config_file, encoding="utf-8-sig")
    config_local_file = os.path.join(path, 'config-local.ini')
    if os.path.isfile(config_local_file):
        conf.read(config_local_file, encoding="utf-8-sig")
    # 兼容不同的布尔值判断，需要用 params 参数获取
    true = ['1', 'true', 'True']
    false = ['0', 'false', 'False']
    params = {}
    for section in conf.sections():
        params[section] = {}
        for param in conf.items(section):
            if param[1] in true:
                params[section][param[0]] = True
            elif param[1] in false:
                params[section][param[0]] = False
            else:
                params[section][param[0]] = param[1]
