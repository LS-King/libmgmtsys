#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2020/6/26 22:21
# @Author      : Peter
# @Description : 
# @File        : tools.py
# @Software    : PyCharm
import pymysql
import datetime
import mypkg.database


# 检查分类信息是否合法
def check_classification(new_classification):
    flag = True
    while flag:
        if new_classification.isdigit():
            flag = False
        else:
            new_classification = input("您输入的分类信息有误，请重新输入：")
    return new_classification


# 检查入库数量是否合法
def check_num(new_num):
    flag = True
    while flag:
        if new_num.isdigit():
            new_num_digit = int(new_num)
            if new_num_digit > 0:
                flag = False
            else:
                new_num = input("您输入的数量有误，请重新输入：")
        else:
            new_num = input("您输入的数量有误，请重新输入：")
    return new_num


# 检查出版年份是否合法
def check_pubyear(new_pubyear_str):
    flag = True
    while flag:
        if new_pubyear_str.isdigit():
            new_pubyear = int(new_pubyear_str)
            if (1920 < new_pubyear < 2035) and new_pubyear <= int(datetime.datetime.now().year):
                flag = False
            else:
                new_pubyear_str = input("您输入的出版年份有误，请重新输入：")
        else:
            new_pubyear_str = input("您输入的出版年份有误，请重新输入：")
    return new_pubyear_str


# 检查图书ISBN号是否重复或者有误
def check_ISBN(book_list, new_ISBN):
    flag = True
    while flag:
        # 先检查是不是纯数字再去考虑是否重复的事情，如果不是纯数字直接pass
        if new_ISBN.isdigit():
            for i in range(len(book_list)):
                if book_list[i]['ISBN'] == new_ISBN:
                    new_ISBN = check_ISBN(book_list, input("您输入的ISBN号重复，请重新输入："))
            flag = False
        else:
            new_ISBN = input("您输入的ISBN号有误，请重新输入：")
    return new_ISBN


# 检查图书ISBN号是否存在
def check_ISBN_exist(book_list, ISBN):
    flag = True
    while flag:
        # 先检查是不是纯数字再去考虑是否存在的事情，如果不是纯数字直接pass
        if ISBN.isdigit():
            for book in book_list:
                if book['ISBN'] == ISBN:
                    flag = False
                    break
            if flag:
                ISBN = check_ISBN_exist(book_list, input("您输入的ISBN号不存在，请重新输入："))
        else:
            ISBN = input("您输入的ISBN号有误，请重新输入：")
    return ISBN


# 检查内部人员信息是否存在
def isexist_inner_customer(code):
    flag = False
    connection = mypkg.database.get_connection()
    # 获取游标 对数据库进行操作 并且将返回值设置为字典类型
    cur = connection.cursor(cursor=pymysql.cursors.DictCursor)
    # 写sql语句
    sql = "select * from inner_customers where code='%s'"
    try:
        cur.execute(sql % code)
        customer = cur.fetchall()
        if type(customer) == list:
            flag = True
    except Exception as e:
        # 错误回滚
        connection.rollback()
        raise e
    finally:
        cur.close()
        connection.close()  # 关闭连接
    return flag


# 检查外部人员信息是否存在
def isexist_outer_customer(code):
    flag = False
    connection = mypkg.database.get_connection()
    # 获取游标 对数据库进行操作 并且将返回值设置为字典类型
    cur = connection.cursor(cursor=pymysql.cursors.DictCursor)
    # 写sql语句
    sql = "select * from outer_customers where code='%s'"
    try:
        cur.execute(sql % code)
        customer = cur.fetchall()
        if type(customer) == list:
            flag = True
    except Exception as e:
        # 错误回滚
        connection.rollback()
        raise e
    finally:
        cur.close()
        connection.close()  # 关闭连接
    return flag


# 获取内部人员id
def get_inner_id(code):
    connection = mypkg.database.get_connection()
    # 获取游标 对数据库进行操作 并且将返回值设置为字典类型
    cur = connection.cursor(cursor=pymysql.cursors.DictCursor)
    # 写sql语句
    sql = "select id from inner_customers where code='%s'"
    # 从custom表中取出用户id
    try:
        cur.execute(sql % code)
        info = cur.fetchall()
        id = info[0]['id']
        return id
    except Exception as e:
        # 错误回滚
        connection.rollback()
        raise e
    finally:
        cur.close()
        connection.close()  # 关闭连接


# 获取外部人员id
def get_outer_id(code):
    connection = mypkg.database.get_connection()
    # 获取游标 对数据库进行操作 并且将返回值设置为字典类型
    cur = connection.cursor(cursor=pymysql.cursors.DictCursor)
    # 写sql语句
    sql = "select id from outer_customers where code='%s'"
    # 从custom表中取出用户id
    try:
        cur.execute(sql % code)
        info = cur.fetchall()
        id = info[0]['id']
        return id
    except Exception as e:
        # 错误回滚
        connection.rollback()
        raise e
    finally:
        cur.close()
        connection.close()  # 关闭连接


# 检查借阅数目是否非法
def islegal_num(type, num):
    if type == 0:
        if num > 2 or num < 0:
            return False
        else:
            return True
    elif type == 1:
        if num > 5 or num < 0:
            return False
        else:
            return True


# 检查是否有库存
def isexist_book(book_list, ISBN):
    for book in book_list:
        if book['ISBN'] == ISBN:
            if book['num'] >= 1:
                return True
            else:
                return False
    return False


# 计算超期天数
def calc_overdue(type, id, ISBN):
    connection = mypkg.database.get_connection()
    # 获取游标 对数据库进行操作 并且将返回值设置为字典类型
    cur = connection.cursor(cursor=pymysql.cursors.DictCursor)
    # 写sql语句
    sql = "select date from customer_book where id=%d and ISBN='%s'"
    try:
        cur.execute(sql % (id, ISBN))
        info = cur.fetchall()
        date = info[0]['date']
    except Exception as e:
        # 错误回滚
        connection.rollback()
        raise e
    finally:
        cur.close()
        connection.close()  # 关闭连接
    delta = (date - datetime.datetime.now().date()).days
    if type == 0:
        if delta <= 30:
            return 0
        else:
            return delta - 30
    elif type == 1:
        if delta <= 60:
            return 0
        else:
            return delta - 60