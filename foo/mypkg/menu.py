#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2020/6/26 21:56
# @Author      : Peter
# @Description : 
# @File        : menu.py
# @Software    : PyCharm


# 主菜单
def display_menu():
    print()
    print("-" * 30)
    print("       图书馆综合管理系统      ")
    print("       1.图书信息录入")
    print("       2.人员信息录入")
    print("       3.图书信息查询")
    print("       4.图书借阅")
    print("       5.图书归还")
    print("       6.退出系统")
    print("-" * 30)


# 图书录入菜单
def display_book_menu():
    print("-" * 30)
    print("       1.新书入库")
    print("       2.库存增减")
    print("       3.返回上级菜单")
    print("-" * 30)


# 图书查询菜单
def display_find_menu():
    print("-" * 30)
    print("       1.展示全部图书信息")
    print("       2.查询特定图书信息")
    print("       3.返回上级菜单")
    print("-" * 30)


# 图书查询方式选择菜单
def display_find_one_menu():
    print("-" * 30)
    print("       1.按ISBN号查询")
    print("       2.按书名查询")
    print("       3.按作者查询")
    print("-" * 30)


# 人员信息录入选择菜单
def display_customer_menu():
    print("-" * 30)
    print("       1.内部人员信息录入")
    print("       2.外来人员信息录入")
    print("       3.返回上级菜单")
    print("-" * 30)


# 图书借阅菜单
def display_borrow_menu():
    print("-" * 30)
    print("       1.内部人员借阅")
    print("       2.外来人员借阅")
    print("       3.返回上级菜单")
    print("-" * 30)


# 图书归还菜单
def display_return_menu():
    print("-" * 30)
    print("       1.内部人员归还")
    print("       2.外来人员归还")
    print("       3.返回上级菜单")
    print("-" * 30)