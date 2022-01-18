# -*- coding: utf-8 -*-
# @Time    : 2021/10/24 1:12 下午 
# @Author  : xujunpeng
from elasticsearch import Elasticsearch

from elasticsearch import Elasticsearch

es_ip = 'http://42.193.113.198'
es_port = '138086'
es = Elasticsearch(
    [es_ip]
    , http_auth=('elastic', 'prrvUdZNg7CQm5LQ4dWWmLCZjX0KCZU9')
    , port=es_port
)
es.indices.create()