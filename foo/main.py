import pymysql
import datetime


book_list = []  # 存储图书信息字典，图书信息用字典存，再用列表存储字典
customer_list = []   # 存储人员信息字典，人员信息用字典存，再用列表存储字典


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


# 选择序号的获得
def get_choice():
    selected_key = input("请输入选择的序号：")
    return selected_key


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
def check_ISBN(new_ISBN):
    flag = True
    while flag:
        # 先检查是不是纯数字再去考虑是否重复的事情，如果不是纯数字直接pass
        if new_ISBN.isdigit():
            for i in range(len(book_list)):
                if book_list[i]['ISBN'] == new_ISBN:
                    new_ISBN = check_ISBN(input("您输入的ISBN号重复，请重新输入："))
            flag = False
        else:
            new_ISBN = input("您输入的ISBN号有误，请重新输入：")
    return new_ISBN


# 检查图书ISBN号是否存在
def check_ISBN_exist(ISBN):
    flag = True
    while flag:
        # 先检查是不是纯数字再去考虑是否存在的事情，如果不是纯数字直接pass
        if ISBN.isdigit():
            for book in book_list:
                if book['ISBN'] == ISBN:
                    flag = False
                    break
            if flag:
                ISBN = check_ISBN_exist(input("您输入的ISBN号不存在，请重新输入："))
        else:
            ISBN = input("您输入的ISBN号有误，请重新输入：")
    return ISBN


# 添加新入库图书信息
def add_new_book():
    new_info = {}
    new_ISBN = check_ISBN(input("请输入图书ISBN号："))
    new_info['ISBN'] = new_ISBN
    new_name = input("请输入书名：")
    new_info['name'] = new_name
    new_author = input("请输入作者：")
    new_info['author'] = new_author
    new_publisher = input("请输入出版社：")
    new_info['publisher'] = new_publisher
    new_pubyear = check_pubyear(input("请输入出版年份："))
    new_info['pubyear'] = int(new_pubyear)
    new_classification = check_classification(input("请输入图书分类："))
    new_info['classification'] = int(new_classification)
    new_num = check_num(input("请输入入库数量："))
    new_info["num"] = int(new_num)
    book_list.append(new_info)
    # 将新图书信息添加到数据库中
    book_insert(new_info)
    print("添加成功！")


# 修改图书库存信息
def update_book():
    """
        要做到内存中的数据与数据库中数据同时修改的话，我做的是先修改本地的数据，
        再对数据库中的数据做修改
    """
    ISBN = check_ISBN_exist(input("请输入图书的ISBN号："))
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
    update_book_num(ISBN, num)


# 库存变动
def update_book_num(ISBN, num):
    connection = get_connection()
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
def find_all():
    print("=" * 56)
    global book_list
    book_list = book_query()
    print("ISBN号    书名    作者     出版社     出版年份 分类 数量")
    for book in book_list:
        print("%s %s %s %s %d %d %d" % (book['ISBN'], book['name'], book['author'], book['publisher'], book['pubyear'], book['classification'], book['num']))
    print("=" * 56)


# 查找特定图书信息
def find_one():
    display_find_one_menu()
    find_one_key = get_choice()
    if find_one_key == '1':
        find_one_byISBN()
    elif find_one_key == '2':
        find_one_byname()
    elif find_one_key == '3':
        find_one_byauthor()


# 通过ISBN号查找图书
def find_one_byISBN():
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
def find_one_byname():
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
def find_one_byauthor():
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


# 检查内部人员信息是否存在
def isexist_inner_customer(code):
    flag = False
    connection = get_connection()
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
    connection = get_connection()
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


# 新增内部人员
def insert_inner_customer():
    flag = True
    code = input("请输入学号/工号：")
    while flag:
        if code.isdigit():
            if not isexist_inner_customer(code):
                flag = False
                name = input("请输入姓名：")
                connection = get_connection()
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
                    # 写入本地人员列表
                    customer_list.append(customer[0])
                    # 写入inner_customers表
                    cur.execute(sql3 % (customer[0]['id'],code,name))
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
def insert_outer_customer():
    flag = True
    code = input("请输入身份证号：")
    while flag:
        if code.isdigit():
            if not isexist_outer_customer(code):
                flag = False
                name = input("请输入姓名：")
                connection = get_connection()
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
                    # 写入本地人员列表
                    customer_list.append(customer[0])
                    # 写入inner_customers表
                    cur.execute(sql3 % (customer[0]['id'],code,name))
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


# 获取内部人员id
def get_inner_id(code):
    connection = get_connection()
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
    connection = get_connection()
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
def isexist_book(ISBN):
    for book in book_list:
        if book['ISBN'] == ISBN:
            if book['num'] >= 1:
                return True
            else:
                return False
    return False


# 内部人员图书借阅
def inner_book_borrow():
    flag = True
    code = input("请输入学号/工号：")
    while flag:
        if code.isdigit():
            if isexist_inner_customer(code):
                flag = False
                ISBN = check_ISBN_exist(input("请输入需借阅图书的ISBN号："))
                id = get_inner_id(code)
                borrowed_num = 0
                for customer in customer_list:
                    if customer['id'] == id:
                        borrowed_num = customer['borrowed_num']
                        break
                if islegal_num(1, borrowed_num + 1):
                    if isexist_book(ISBN):
                        connection = get_connection()
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
                                    # 写入本地
                                    book['num'] = num
                                    break
                            for customer in customer_list:
                                if customer['id'] == id:
                                    borrowed_num = customer['borrowed_num'] + 1
                                    # 写入本地
                                    customer['borrowed_num'] = borrowed_num
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
def outer_book_borrow():
    flag = True
    code = input("请输入身份证号：")
    while flag:
        if code.isdigit():
            if isexist_outer_customer(code):
                flag = False
                ISBN = check_ISBN_exist(input("请输入需借阅图书的ISBN号："))
                id = get_outer_id(code)
                borrowed_num = 0
                for customer in customer_list:
                    if customer['id'] == id:
                        borrowed_num = customer['borrowed_num']
                        break
                if islegal_num(0, borrowed_num + 1):
                    if isexist_book(ISBN):
                        connection = get_connection()
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
                                    # 写入本地
                                    book['num'] = num
                                    break
                            for customer in customer_list:
                                if customer['id'] == id:
                                    borrowed_num = customer['borrowed_num'] + 1
                                    # 写入本地
                                    customer['borrowed_num'] = borrowed_num
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


# 计算超期天数
def calc_overdue(type, id, ISBN):
    connection = get_connection()
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
def inner_book_return():
    flag = True
    code = input("请输入学号/工号：")
    while flag:
        if code.isdigit():
            if isexist_inner_customer(code):
                flag = False
                ISBN = check_ISBN_exist(input("请输入需归还图书的ISBN号："))
                id = get_inner_id(code)
                overdue = calc_overdue(1, id, ISBN)
                # 如果逾期先交罚款
                if overdue > 0:
                    if not pay_fine(1, overdue):
                        return
                return_book(id, ISBN)
            else:
                print("您输入的人员信息不存在！")
                return
        else:
            code = input("输入有误，请重新输入学号/工号：")


# 外部人员图书归还
def outer_book_return():
    flag = True
    code = input("请输入身份证号：")
    while flag:
        if code.isdigit():
            if isexist_outer_customer(code):
                flag = False
                ISBN = check_ISBN_exist(input("请输入需归还图书的ISBN号："))
                id = get_outer_id(code)
                overdue = calc_overdue(0, id, ISBN)
                # 如果逾期先交罚款
                if overdue > 0:
                    if not pay_fine(0, overdue):
                        return
                return_book(id, ISBN)
            else:
                print("您输入的人员信息不存在！")
                return
        else:
            code = input("输入有误，请重新输入学号/工号：")


# 还书
def return_book(id, ISBN):
    connection = get_connection()
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
                # 写入本地
                book['num'] = num
                break
        for customer in customer_list:
            if customer['id'] == id:
                borrowed_num = customer['borrowed_num'] - 1
                # 写入本地
                customer['borrowed_num'] = borrowed_num
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


# 获取数据库连接的方法
def get_connection():
    connection = pymysql.connect(host="localhost", user="root", password="450052", database="libmgmt", port=3306)
    return connection


# 初始化的时候从数据库中获取图书信息
def book_query():
    connection = get_connection()
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


# 初始化的时候从数据库中获取人员信息
def customer_query():
    connection = get_connection()
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


# 初始化函数，从数据库中查询到的赋值给book_list
def book_init():
    try:
        global book_list
        book_list = book_query()
        print("成功获取数据库中图书数据！")
    except Exception as e:
        raise e


# 初始化函数，从数据库中查询到的赋值给customer_list
def customer_init():
    try:
        global customer_list
        customer_list = customer_query()
        print("成功获取数据库中人员数据！")
    except Exception as e:
        raise e


# 添加图书 -- 直接添加到数据库里面
def book_insert(book):
    connection = get_connection()
    # 获取游标 对数据库进行操作 并且将返回值设置为字典类型
    cur = connection.cursor(cursor=pymysql.cursors.DictCursor)
    # 写sql语句
    sql = "insert into books(ISBN,name,author,publisher,pubyear,classification,num) values('%s','%s','%s','%s',%d,%d,%d)"
    ISBN = book['ISBN']
    name = book['name']
    author = book['author']
    publisher = book['publisher']
    pubyear = book['pubyear']
    classification = book['classification']
    num = book['num']
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


def main():
    book_init()
    customer_init()
    exit_name = True
    while exit_name:
        display_menu()
        key = get_choice()
        if key == '1':
            display_book_menu()
            book_key = get_choice()
            if book_key == '1':
                add_new_book()
            elif book_key == '2':
                update_book()
        elif key == '2':
            display_customer_menu()
            customer_key = get_choice()
            if customer_key == '1':
                insert_inner_customer()
            elif customer_key == '2':
                insert_outer_customer()
        elif key == '3':
            display_find_menu()
            find_key = get_choice()
            if find_key == '1':
                find_all()
            elif find_key == '2':
                find_one()
        elif key == '4':
            display_borrow_menu()
            borrow_key = get_choice()
            if borrow_key == '1':
                inner_book_borrow()
            elif borrow_key == '2':
                outer_book_borrow()
        elif key == '5':
            display_return_menu()
            return_key = get_choice()
            if return_key == '1':
                inner_book_return()
            elif return_key == '2':
                outer_book_return()
        elif key == '6':
            exit_name = False
        else:
            print("请输入正确的数值！")

if __name__ == '__main__':
    main()