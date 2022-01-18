# -*- coding: utf-8 -*-
# @Time    : 2021/11/13 1:47 下午 
# @Author  : xujunpeng
from app import app
from confluent_kafka import Producer

KafkaProducer = Producer({'bootstrap.servers': app.config["KAFKA_SERVERS"]})
