#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2020/6/26 22:20
# @Author      : Peter
# @Description : 用户信息及交互相关函数
# @File        : customer.py
# @Software    : PyCharm
import pymysql
import datetime
import mypkg.database
import mypkg.tools


# 初始化的时候从数据库中获取人员信息
def customer_query():
    connection = mypkg.database.get_connection()
    # 获取游标 对数据库进行操作 并且将返回值设置为字典类型
    cur = connection.cursor(cursor=pymysql.cursors.DictCursor)
    # 写sql语句
    sql = "select * from customers"
    try:
        cur.execute(sql)
        customers = cur.fetchall()
        """
            此处判断很重要，如果数据库中没有记录，则会结果是一个空的元组类型，
            如果有记录，则结果是list类型，所以可以根据类型来判断数据库是否为空，
            如果不是就返回一个空列表。
        """
        if type(customers) == list:
            return customers
        else:
            return []
    except Exception as e:
        raise e
    finally:
        cur.close()
        connection.close()  # 关闭连接


# 新增内部人员
def insert_inner_customer(customer_list):
    flag = True
    code = input("请输入学号/工号：")
    while flag:
        if code.isdigit():
            if not mypkg.tools.isexist_inner_customer(code):
                flag = False
                name = input("请输入姓名：")
                connection = mypkg.database.get_connection()
                # 获取游标 对数据库进行操作 并且将返回值设置为字典类型
                cur = connection.cursor(cursor=pymysql.cursors.DictCursor)
                # 写sql语句
                sql1 = "insert into customers(name,type) values('%s',%d)"
                sql2 = "select * from customers where name='%s'"
                sql3 = "insert into inner_customers(id,code,name) values(%d,'%s','%s')"
                try:
                    # 写入customer表
                    cur.execute(sql1 % (name, 1))
                    connection.commit()
                    cur.execute(sql2 % name)
                    customer = cur.fetchall()
                    # 写入inner_customers表
                    cur.execute(sql3 % (customer[0]['id'], code, name))
                    connection.commit()
                    print("内部人员信息添加成功！")
                except Exception as e:
                    # 错误回滚
                    connection.rollback()
                    raise e
                finally:
                    cur.close()
                    connection.close()  # 关闭连接
            else:
                print("该信息已在人员信息库中录入！")
                return
        else:
            code = input("输入有误，请重新输入学号/工号：")


# 新增外部人员
def insert_outer_customer(customer_list):
    flag = True
    code = input("请输入身份证号：")
    while flag:
        if code.isdigit():
            if not mypkg.tools.isexist_outer_customer(code):
                flag = False
                name = input("请输入姓名：")
                connection = mypkg.database.get_connection()
                # 获取游标 对数据库进行操作 并且将返回值设置为字典类型
                cur = connection.cursor(cursor=pymysql.cursors.DictCursor)
                # 写sql语句
                sql1 = "insert into customers(name,type) values('%s',%d)"
                sql2 = "select * from customers where name='%s'"
                sql3 = "insert into outer_customers(id,code,name) values(%d,'%s','%s')"
                try:
                    # 写入customer表
                    cur.execute(sql1 % (name, 0))
                    connection.commit()
                    cur.execute(sql2 % name)
                    customer = cur.fetchall()
                    # 写入inner_customers表
                    cur.execute(sql3 % (customer[0]['id'], code, name))
                    connection.commit()
                    print("外部人员信息添加成功！")
                except Exception as e:
                    # 错误回滚
                    connection.rollback()
                    raise e
                finally:
                    cur.close()
                    connection.close()  # 关闭连接
            else:
                print("该信息已在人员信息库中录入！")
                return
        else:
            code = input("输入有误，请重新输入身份证号：")


# 内部人员图书借阅
def inner_borrow_book(customer_list, book_list):
    flag = True
    code = input("请输入学号/工号：")
    while flag:
        if code.isdigit():
            if mypkg.tools.isexist_inner_customer(code):
                flag = False
                ISBN = mypkg.tools.check_ISBN_exist(book_list, input("请输入需借阅图书的ISBN号："))
                id = mypkg.tools.get_inner_id(code)
                borrowed_num = 0
                for customer in customer_list:
                    if customer['id'] == id:
                        borrowed_num = customer['borrowed_num']
                        break
                if mypkg.tools.islegal_num(1, borrowed_num + 1):
                    if mypkg.tools.isexist_book(book_list, ISBN):
                        connection = mypkg.database.get_connection()
                        # 获取游标 对数据库进行操作 并且将返回值设置为字典类型
                        cur = connection.cursor(cursor=pymysql.cursors.DictCursor)
                        # 写sql语句
                        sql1 = "insert into customer_book(id,ISBN,date) values(%d,'%s','%s')"
                        sql2 = "update books set num=%d where ISBN='%s'"
                        sql3 = "update customers set borrowed_num=%d where id=%d"
                        try:
                            # 写入customer表
                            cur.execute(sql1 % (id, ISBN, datetime.datetime.now().date()))
                            connection.commit()
                            num = 0
                            borrowed_num = 0
                            for book in book_list:
                                if book['ISBN'] == ISBN:
                                    num = book['num'] - 1
                                    break
                            for customer in customer_list:
                                if customer['id'] == id:
                                    borrowed_num = customer['borrowed_num'] + 1
                            cur.execute(sql2 % (num, ISBN))
                            connection.commit()
                            cur.execute(sql3 % (borrowed_num, id))
                            connection.commit()
                            print("借书成功！")
                        except Exception as e:
                            # 错误回滚
                            connection.rollback()
                            raise e
                        finally:
                            cur.close()
                            connection.close()  # 关闭连接
                    else:
                        print("您需借阅的图书库存不足！")
                        return
                else:
                    print("您暂时不能借阅此图书，请检查您是否超额借阅！")
                    return
            else:
                print("您输入的人员信息不存在！")
                return
        else:
            code = input("输入有误，请重新输入学号/工号：")


# 外部人员图书借阅
def outer_borrow_book(customer_list, book_list):
    flag = True
    code = input("请输入身份证号：")
    while flag:
        if code.isdigit():
            if mypkg.tools.isexist_outer_customer(code):
                flag = False
                ISBN = mypkg.tools.check_ISBN_exist(book_list, input("请输入需借阅图书的ISBN号："))
                id = mypkg.tools.get_outer_id(code)
                borrowed_num = 0
                for customer in customer_list:
                    if customer['id'] == id:
                        borrowed_num = customer['borrowed_num']
                        break
                if mypkg.tools.islegal_num(0, borrowed_num + 1):
                    if mypkg.tools.isexist_book(book_list, ISBN):
                        connection = mypkg.database.get_connection()
                        # 获取游标 对数据库进行操作 并且将返回值设置为字典类型
                        cur = connection.cursor(cursor=pymysql.cursors.DictCursor)
                        # 写sql语句
                        sql1 = "insert into customer_book(id,ISBN,date) values(%d,'%s','%s')"
                        sql2 = "update books set num=%d where ISBN='%s'"
                        sql3 = "update customers set borrowed_num=%d where id=%d"
                        try:
                            # 写入customer表
                            cur.execute(sql1 % (id, ISBN, datetime.datetime.now().date()))
                            connection.commit()
                            num = 0
                            borrowed_num = 0
                            for book in book_list:
                                if book['ISBN'] == ISBN:
                                    num = book['num'] - 1
                                    break
                            for customer in customer_list:
                                if customer['id'] == id:
                                    borrowed_num = customer['borrowed_num'] + 1
                                    break
                            cur.execute(sql2 % (num, ISBN))
                            connection.commit()
                            cur.execute(sql3 % (borrowed_num, id))
                            connection.commit()
                            print("借书成功！")
                        except Exception as e:
                            # 错误回滚
                            connection.rollback()
                            raise e
                        finally:
                            cur.close()
                            connection.close()  # 关闭连接
                    else:
                        print("您需借阅的图书库存不足！")
                        return
                else:
                    print("您暂时不能借阅此图书，请检查您是否超额借阅！")
                    return
            else:
                print("您输入的人员信息不存在！")
                return
        else:
            code = input("输入有误，请重新输入身份证号：")


# 支付逾期罚款
def pay_fine(type, overdue):
    fine = 0
    if type == 0:
        fine = 3 * overdue
    elif type == 1:
        fine = overdue
    print("您需缴纳" + fine + "元的逾期罚款！")
    flag = input("是否已缴纳？（是-1，否-0）")
    if flag:
        print("罚款缴纳成功！")
        return True
    else:
        print("请您尽快缴纳罚款！")
        return False


# 内部人员图书归还
def inner_return_book(customer_list, book_list):
    flag = True
    code = input("请输入学号/工号：")
    while flag:
        if code.isdigit():
            if mypkg.tools.isexist_inner_customer(code):
                flag = False
                ISBN = mypkg.tools.check_ISBN_exist(book_list, input("请输入需归还图书的ISBN号："))
                id = mypkg.tools.get_inner_id(code)
                overdue = mypkg.tools.calc_overdue(1, id, ISBN)
                # 如果逾期先交罚款
                if overdue > 0:
                    if not pay_fine(1, overdue):
                        return
                return_book(customer_list, book_list, id, ISBN)
            else:
                print("您输入的人员信息不存在！")
                return
        else:
            code = input("输入有误，请重新输入学号/工号：")


# 外部人员图书归还
def outer_return_book(customer_list, book_list):
    flag = True
    code = input("请输入身份证号：")
    while flag:
        if code.isdigit():
            if mypkg.tools.isexist_outer_customer(code):
                flag = False
                ISBN = mypkg.tools.check_ISBN_exist(book_list, input("请输入需归还图书的ISBN号："))
                id = mypkg.tools.get_outer_id(code)
                overdue = mypkg.tools.calc_overdue(0, id, ISBN)
                # 如果逾期先交罚款
                if overdue > 0:
                    if not pay_fine(0, overdue):
                        return
                return_book(customer_list, book_list, id, ISBN)
            else:
                print("您输入的人员信息不存在！")
                return
        else:
            code = input("输入有误，请重新输入学号/工号：")


# 还书
def return_book(customer_list, book_list, id, ISBN):
    connection = mypkg.database.get_connection()
    # 获取游标 对数据库进行操作 并且将返回值设置为字典类型
    cur = connection.cursor(cursor=pymysql.cursors.DictCursor)
    # 写sql语句
    sql1 = "delete from customer_book where id=%d and ISBN='%s'"
    sql2 = "update books set num=%d where ISBN='%s'"
    sql3 = "update customers set borrowed_num=%d where id=%d"
    try:
        # 删除借书记录
        cur.execute(sql1 % (id, ISBN))
        connection.commit()
        num = 0
        borrowed_num = 0
        for book in book_list:
            if book['ISBN'] == ISBN:
                num = book['num'] + 1
                break
        for customer in customer_list:
            if customer['id'] == id:
                borrowed_num = customer['borrowed_num'] - 1
        cur.execute(sql2 % (num, ISBN))
        connection.commit()
        cur.execute(sql3 % (borrowed_num, id))
        connection.commit()
        print("还书成功！")
    except Exception as e:
        # 错误回滚
        connection.rollback()
        raise e
    finally:
        cur.close()
        connection.close()  # 关闭连接