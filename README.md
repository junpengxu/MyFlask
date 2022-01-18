# MyFlask
- 使用flask搭建一个web后端服务的脚手架

## 项目结构
```
├── Dockerfile                      # dockerfile
├── LICENSE
├── README.md
├── app                             # 框架的服务主要实现模块
│   ├── __init__.py                 # 服务的初始化
│   ├── admin                       # 单独设置了后台模块
│   │   ├── __init__.py
│   │   └── readme.md
│   ├── base                        # 定义了基类模块
│   │   ├── __init__.py
│   │   ├── base_controller.py      # controller层基类 
│   │   ├── base_enum.py            # 枚举基类
│   │   ├── base_logger.py          # logger基类
│   │   ├── base_model.py           # model层基类
│   │   ├── base_request.py         # 针对request进行一次封装，所有的针对第三方的请求通过这个request基类实现
│   │   ├── base_view.py            # view层基类
│   ├── celery                      # 异步任务的模块
│   │   ├── __init__.py             # celery模块的初始化
│   │   ├── beat.py                 # 定时任务
│   │   └── tasks.py                # 异步任务
│   ├── controller                  # 定义了服务的controller层
│   │   ├── Ping.py
│   │   ├── __init__.py
│   ├── enum                        # 管理服务的枚举
│   │   ├── __init__.py
│   │   ├── enum_code.py            # 定义了业务想管的枚举
│   │   └── status_code.py          # 定义了系统状态的枚举
│   ├── model                       # 定义了服务的model层
│   │   ├── __init__.py             # 初始化model
│   │   └── ping.py
│   ├── unittest                    # 实现单元测试等
│   │   └── __init__.py
│   ├── urls.py                     # 管理了服务的路由层
│   ├── utils                       # 定义了各种工具类
│   │   ├── grafana_transport.py    # 重新封装grafana的client
│   │   ├── __init__.py             
│   │   ├── decorator               # 定义各种自定义装饰器
│   │   ├── img_upload.py           # 图片上传模块
│   │   ├── kafka.py                # kafka client 封装
│   │   ├── lock.py                 # 管理了各种锁
│   │   ├── logger.py               # 自定义logger
│   │   ├── monitor.py              # 耗时监控
│   │   ├── singleton.py            # 单利装饰器
│   │   └── trace.py                # 封装了zipkin的client
│   └── view                        # 定义了服务的view层
│       ├── __init__.py
│       └── ping.py
├── config                          # 配置文件
│   ├── __init__.py
│   ├── celery_config.py            # celery配置
│   ├── online.py                   # 服务的线上配置
│   └── test.py                     # 服务的测试配置
├── manage.py                       # 启动文件
├── migrations                      # 数据库变动前期管理模块
│   ├── README
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions
│       ├── __pycache__
│       ├── c74c3a14facb_init.py
└── requirements.txt                # 依赖文件

```
## 组件
| 组件       | 描述   |  状态  |
| :--------  | :-----  | :----:  |
| mysql | 数据库 |done|
| redis | 缓存数据库 |done|
| celery | 完成定时任务，异步任务 |done|
| kafka | 日志记录，记录下了每一条请求，可用于后续的各种分析 |done|
| zipkin | 全链路监控 |done|
| sentry | 异常管理 |done|
| grafana | 监控与数据统计 |done|
| flink | 自定义各种统计任务，etl等 |doing|
| elasticsearch | 用于提供数据搜索，自定义数据排序等功能 |todo|

## 基础服务
| 功能点       | 描述   |  状态  |
| :--------  | :-----  | :----:  |
| 请求上报 | 在base_view层，在访问的url到映射view层的过程中，将请求的数据结构化之后，写入到kafka |done|
| 链路监控 | 封装了Trace类，可在需要进行链路监控的地方手动上报数据。通过继承元类TraceDecorator实现针对某个类下的所有函数进行了一次Trace装饰器的封装，这里需要注意的一点，如果类的方法已经有过装饰器，则TraceDecorator失效 |done|
| 异常监控 | 继承了sentry，可自动上报flask服务检测到的异常，同时封装了log_exception可以实现手动上报异常 |done|
| 耗时监控 | grafana_transport 封装了自定义打点 |done|

## 自定义功能
| 功能点       | 描述   |  状态  |
| :--------  | :-----  | :----:  |
| 主从数据库 |  |done|
| 服务调用链路监控 | 服务间请求通过在header中携带trace信息实现 |todo|
| 线程监控 | 监控主进程fork出来线程的关系，集成到trace |todo|
| celery任务监控 | 串联起请求所触发的所有celery任务，集成到trace |todo|


## 使用介绍
1. urls.py 中设置路由映射
2. view层实现请求接入以及数据处理与业务数据
3. controller层实现对model层的操作
4. model层定义数据结构，model层已经设置了软删除，查询的sql会自动拼接is_delete=False