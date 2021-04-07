一个使用 Python 实现的 Linux 服务器运维小工具，满足条件时使用钉钉机器人发出警报。

使用 Python 3.7+ 版本测试通过。

### 功能
- 检查硬盘占用
    
  可指定检查多个挂载路径，以及占用百分比阈值，超过阈值发出警报；
  
- 检查进程运行情况

  配置需要检查的进程查找字符串，检查运行情况，进程不存在时发出警报；

- 检查 supervisor 守护程序守护的进程运行情况

  非 RUNNING 状态时发出报警；

### 安装

```bash
clone git@github.com:hsu1943/sys-status.git
cd sys-status
pip install -r ./requirement.txt
```

### 配置

复制配置示例

```bash
cp ./config.ini ./config-local.ini
```

编辑 `config-local.ini`，按照自己的需求配置。

### 运行

使用 `crontab` 运行脚本 `run.py` 即可。


  