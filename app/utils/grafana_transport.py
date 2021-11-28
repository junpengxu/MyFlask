# -*- coding: utf-8 -*-
# @Time    : 2021/11/3 11:20 下午
# @Author  : xujunpeng
import os
import socket
import threading
import time

from app import app
from app.utils.singleton import singleton
from influxdb import InfluxDBClient
from datetime import datetime, timezone, timedelta
from multiprocessing import Queue

import atexit


@singleton
class GrafanaTransport:
    def __init__(self):

        self.cli = InfluxDBClient(
            host=app.config["GRAFANA_HOST"],
            port=app.config["GRAFANA_PORT"],
            database=app.config["GRAFANA_DB"],
            udp_port=app.config["GRAFANA_UDP_PORT"],
            use_udp=app.config["GRAFANA_USE_UDP"]
        )

        self.data_stream = Queue()
        threading.Thread(target=self.working, args=(self.data_stream,)).start()

    def working(self, data_stream):
        while True:
            send_data = []
            try:
                # TODO 这样会造成丢失打点, 需要正确处理程序退出
                for i in range(32):
                    send_data.append(data_stream.get(block=True, timeout=1))
            except Exception as e:
                print(e)
            finally:
                if not send_data:
                    time.sleep(3)
                else:
                    self.cli.write_points(send_data)

    def send(self, measurement, tags=None, fields=None):
        # TODO 修改为socket
        # TODO 修改为等待批量发送
        if fields is None:
            fields = {}
        if tags is None:
            tags = {}
        tags.update({
            "host": socket.gethostbyname(socket.gethostname()),
            "pid": os.getpid(),
            "tid": threading.currentThread().ident  # 线程id会太多了。造成计算不过来的
        })
        data = {
            "measurement": measurement,
            "tags": tags,
            "fields": fields,
            "time": str(datetime.now(timezone(timedelta(hours=8)))),
        }
        # 如何实现批量发送
        self.data_stream.put(data)
        # GrafanaTransport.cli.write_points([data])

    # @atexit.register
    # def stop(self):
    #     self._stop_event.set()
