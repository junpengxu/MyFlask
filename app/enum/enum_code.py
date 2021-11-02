# -*- coding: utf-8 -*-
# @Time    : 2020/12/13 2:27 上午
# @Author  : xu.junpeng

from enum import unique
from enum import Enum


@unique
class UserAction(Enum):
    Vote = "vote"
    Collect = "collect"


@unique
class ReplyType(Enum):
    reply = "reply"  # 针对评论的回复（comment的回复）
    comment = "comment"  # 针对内容的评论（第一层回复）


@unique
class UgcType(Enum):
    Topic = "topic"
    Idle = "idle"
    Activity = "activity"
    Reply = "reply"  # 针对评论的回复（comment的回复）
    Comment = "comment"  # 针对内容的评论（第一层回复）
    Chat = "chat"  # 私聊


@unique
class TabType(Enum):
    Topic = "topic"
    Idle = "idle"
    Activity = "activity"


@unique
class UgcCategory(Enum):
    all = 'all'
    topic = "topic"
    idle = "idle"
    activity = "activity"


@unique
class CategoryCN(Enum):
    all = "全部"
    topic = "投稿"
    idle = "闲置"
    activity = "活动"


@unique
class topic_classify(Enum):
    # tougao = "投稿"
    # shiwuzhaoling = "失物招领"
    # zhoaren = "找人"
    # jianzhi = "兼职"
    quanbu = "全部"
    tucaofenxiang = "吐槽分享"
    tiwenqiuzhu = "提问求助"
    shudongshudong = "情感树洞"
    laorenlaoren = "校园捞人"
    jianzhizhaomu = "兼职招募"
    shiwuzhaoling = "失物招领"
    wenjuandiaocha = "问卷调查"
    gonggaoyugao = "公告预告"
    qitatougao = "其他投稿"


@unique
class idle_classify(Enum):
    # huazhuangpin = "化妆品"
    # riyongpin = "日用品"
    # dianzi = "电子设备"
    # close = "服饰"
    # food = "食品"
    # book = "书籍"
    # other = "其他"
    quanbu = "全部"
    shujizhibi = "书籍纸笔"
    piaokazhuanrang = "票卡转让"
    xiannvshichang = "仙女市场"
    yundongzhuangbei = "运动装备"
    daibugongju = "代步工具"
    shuma3C = "数码3C"
    shipinyinliao = "食品饮料"
    xishurichang = "洗漱日常"
    xiebaofushi = "鞋包服饰"
    qitaxianzhi = "其他闲置"


@unique
class activity_classify(Enum):
    # 组局分类
    zixi = "自习"
    dianying = "电影"
    jucan = "聚餐"
    pinche = "拼车"
    pindan = "拼单"
    yundong = "运动"
    youxi = "游戏"
    lvyou = "旅游"
    qita = "其他"


class UgcClassify(Enum):
    dianzi = "dianzi"
    meizhuang = "meizhuang"
    book = "book"
    default = "default"


@unique
class NoticeType(Enum):
    Vote = "vote"  # 点赞
    Collect = "collect"  # 收藏
    Reply = "reply"  # 回复了你的内容
    Comment = "comment"  # 评论了回复
    Chat = "chat"  # 私聊
    All = "all"  # 全部


@unique
class DiscoverType(Enum):
    Report = "report"  # 报道
    Hot = "hot"  # 热门
    Important = "important"  # 重要


@unique
class UserVerifyStatue(Enum):
    Fresh = 0  # 未发起审核
    Auditing = 1  # 审核进行中
    Normal = 2  # 审核通过
    Refuse = 3  # 审核被拒绝
    Mock = 5  # 后台虚拟用户
