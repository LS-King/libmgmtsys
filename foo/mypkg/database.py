#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2020/6/26 22:20
# @Author      : Peter
# @Description : 数据库连接相关函数
# @File        : database.py
# @Software    : PyCharm
import pymysql


# 获取数据库连接的方法
def get_connection():
    connection = pymysql.connect(host="localhost", user="root", password="450052", database="libmgmt", port=3306)
    return connection