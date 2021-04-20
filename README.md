一个使用 Python 实现的 Linux 服务器运维小工具，满足条件时使用钉钉机器人发出警报。

使用 Python 3.7+ 版本测试通过。

### 功能

- 检查硬盘占用
    
  可指定检查多个挂载路径，以及占用百分比阈值，超过阈值发出警报；
  
- 检查进程运行情况

  配置需要检查的进程查找字符串，检查运行情况，进程不存在时发出警报；

- 检查 supervisor 守护程序守护的进程运行情况

  非 RUNNING 状态时发出报警；
 
 - 使用钉钉群机器人报警；
  
 - 提供外部访问api，获取运行情况历史记录；

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

### 接口使用

#### 服务启动：

```bash
python ./main.py
```

服务将会运行在配置文章中指定的端口`service-port`上（默认8008）。

#### 访问
```bash
GET http://127.0.0.1:8008/sys-status/api?gap=900&limit=30
```

#### 请求参数

| 参数名 | 类型 | 示例 | 说明                                     |
| ------ | ---- | ---- | ---------------------------------------- |
| gap    | int  | 900  | 时间间隔，可选 900\|3600\|86400，默认900 |
| limit  | int  | 30   | 数据条数，最大720，默认10                |

#### 响应示例

```json
{
       "code":200,
       "status":"success",
       "data":[
           {
               "time":"2021-04-20 14:30:01",
               "disk_data":[
                   {
                       "filesystem":"/",
                       "size":"40G",
                       "used":"27G",
                       "avail":"11G",
                       "use%":"71%"
                   }
               ],
               "process_data":[
                   {
                       "process":"nginx",
                       "status":"RUNNING"
                   },
                   {
                       "process":"php",
                       "status":"RUNNING"
                   },
                   {
                       "process":"mysql",
                       "status":"RUNNING"
                   }
               ],
               "supervisor_data":[
                   {
                       "service":"mail-queue",
                       "status":"RUNNING"
                   },
                   {
                       "service":"service-gender-ocr",
                       "status":"RUNNING"
                   },
                   {
                       "service":"service-pdf-packer",
                       "status":"RUNNING"
                   }
               ]
           }
       ]
   }
```
