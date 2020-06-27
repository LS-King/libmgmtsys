#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2020/6/26 22:16
# @Author      : Peter
# @Description : 图书信息处理相关函数
# @File        : book.py
# @Software    : PyCharm
import pymysql
import mypkg.database
import mypkg.tools


# 初始化的时候从数据库中获取图书信息
def book_query():
    connection = mypkg.database.get_connection()
    # 获取游标 对数据库进行操作 并且将返回值设置为字典类型
    cur = connection.cursor(cursor=pymysql.cursors.DictCursor)
    # 写sql语句
    sql = "select * from books"
    try:
        cur.execute(sql)
        books = cur.fetchall()
        """
            此处判断很重要，如果数据库中没有记录，则会结果是一个空的元组类型，
            如果有记录，则结果是list类型，所以可以根据类型来判断数据库是否为空，
            如果不是就返回一个空列表。
        """
        if type(books) == list:
            return books
        else:
            return []
    except Exception as e:
        raise e
    finally:
        cur.close()
        connection.close()  # 关闭连接


# 添加新入库图书信息
def insert_book(book_list):
    new_book = {}
    new_ISBN = mypkg.tools.check_ISBN(book_list, input("请输入图书ISBN号："))
    new_book['ISBN'] = new_ISBN
    new_name = input("请输入书名：")
    new_book['name'] = new_name
    new_author = input("请输入作者：")
    new_book['author'] = new_author
    new_publisher = input("请输入出版社：")
    new_book['publisher'] = new_publisher
    new_pubyear = mypkg.tools.check_pubyear(input("请输入出版年份："))
    new_book['pubyear'] = int(new_pubyear)
    new_classification = mypkg.tools.check_classification(input("请输入图书分类："))
    new_book['classification'] = int(new_classification)
    new_num = mypkg.tools.check_num(input("请输入入库数量："))
    new_book["num"] = int(new_num)
    # 将新图书信息添加到数据库中
    connection = mypkg.database.get_connection()
    # 获取游标 对数据库进行操作 并且将返回值设置为字典类型
    cur = connection.cursor(cursor=pymysql.cursors.DictCursor)
    # 写sql语句
    sql = "insert into books(ISBN,name,author,publisher,pubyear,classification,num) values('%s','%s','%s','%s',%d,%d,%d)"
    ISBN = new_book['ISBN']
    name = new_book['name']
    author = new_book['author']
    publisher = new_book['publisher']
    pubyear = new_book['pubyear']
    classification = new_book['classification']
    num = new_book['num']
    # 添加到数据库里面
    try:
        cur.execute(sql % (ISBN, name, author, publisher, pubyear, classification, num))
        connection.commit()
    except Exception as e:
        # 错误回滚
        connection.rollback()
        raise e
    finally:
        cur.close()
        connection.close()  # 关闭连接
    print("添加成功！")


# 修改图书库存信息
def update_book(book_list):
    ISBN = mypkg.tools.check_ISBN_exist(book_list, input("请输入图书的ISBN号："))
    num = 0
    numstr = input("请输入要变动的数目（增加为正数，减少为负数）：")
    flag = True
    while flag:
        if numstr.lstrip('-').isdigit():
            num = int(numstr)
            old_num = 0
            for book in book_list:
                if book['ISBN'] == ISBN:
                    old_num = book['num']
                    break
            if (num + old_num) >= 0:
                num = num + old_num
                flag = False
            else:
                numstr = input("输入有误，请重新输入要变动的数目（增加为正数，减少为负数）：")
        else:
            numstr = input("输入有误，请重新输入要变动的数目（增加为正数，减少为负数）：")
    connection = mypkg.database.get_connection()
    cur = connection.cursor()
    sql = "update books set num=%d where ISBN='%s'"
    try:
        cur.execute(sql % (num, ISBN))
        connection.commit()
        print("操作成功！")
    except Exception as e:
        # 错误回滚
        connection.rollback()
        raise e
    finally:
        cur.close()
        connection.close()  # 关闭连接


# 查询所有图书信息  --是从数据库中查询信息的
def find_all_book(book_list):
    print("=" * 56)
    book_list = book_query()
    print("ISBN号    书名    作者     出版社     出版年份 分类 数量")
    for book in book_list:
        print("%s %s %s %s %d %d %d" % (book['ISBN'], book['name'], book['author'], book['publisher'], book['pubyear'], book['classification'], book['num']))
    print("=" * 56)


# 通过ISBN号查找图书
def find_one_byISBN(book_list):
    ISBN = input("请输入ISBN号：")
    if ISBN.isdigit():
        for book in book_list:
            if book['ISBN'] == ISBN:
                print("已为您查找到以下信息：")
                print("ISBN号    书名    作者     出版社     出版年份 分类 数量")
                print("%s %s %s %s %d %d %d" % (book['ISBN'], book['name'], book['author'], book['publisher'], book['pubyear'], book['classification'], book['num']))
                return
    else:
        print("输入的ISBN号有误！")
        return
    print("没有查到相关图书信息！")


# 通过书名查找图书
def find_one_byname(book_list):
    name = input("请输入书名：")
    books = []
    flag = False
    for book in book_list:
        if name in book['name']:
            books.append(book)
            flag = True
    if flag:
        print("已为您查找到以下信息：")
        print("ISBN号    书名    作者     出版社     出版年份 分类 数量")
        for book in books:
            print("%s %s %s %s %d %d %d" % (book['ISBN'], book['name'], book['author'], book['publisher'], book['pubyear'], book['classification'], book['num']))
    else:
        print("没有查到相关图书信息！")


# 通过作者查找图书
def find_one_byauthor(book_list):
    author = input("请输入作者：")
    books = []
    flag = False
    for book in book_list:
        if author in book['author']:
            books.append(book)
            flag = True
    if flag:
        print("已为您查找到以下信息：")
        print("ISBN号    书名    作者     出版社     出版年份 分类 数量")
        for book in books:
            print("%s %s %s %s %d %d %d" % (book['ISBN'], book['name'], book['author'], book['publisher'], book['pubyear'], book['classification'], book['num']))
    else:
        print("没有查到相关图书信息！")