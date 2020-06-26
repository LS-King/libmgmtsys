import mypkg.menu
import mypkg.tools
import mypkg.book
import mypkg.customer


book_list = []  # 存储图书信息字典，图书信息用字典存，再用列表存储字典
customer_list = []   # 存储人员信息字典，人员信息用字典存，再用列表存储字典


# 选择序号的获得
def get_choice():
    selected_key = input("请输入选择的序号：")
    return selected_key


def main():
    exit_name = True
    while exit_name:
        book_list = mypkg.book.book_query()
        customer_list = mypkg.customer.customer_query()
        mypkg.menu.display_menu()
        key = get_choice()
        if key == '1':
            mypkg.menu.display_book_menu()
            book_key = get_choice()
            if book_key == '1':
                mypkg.book.insert_book(book_list)
            elif book_key == '2':
                mypkg.book.update_book(book_list)
        elif key == '2':
            mypkg.menu.display_customer_menu()
            customer_key = get_choice()
            if customer_key == '1':
                mypkg.customer.insert_inner_customer(customer_list)
            elif customer_key == '2':
                mypkg.customer.insert_outer_customer(customer_list)
        elif key == '3':
            mypkg.menu.display_find_menu()
            find_key = get_choice()
            if find_key == '1':
                mypkg.book.find_all_book(book_list)
            elif find_key == '2':
                mypkg.menu.display_find_one_menu()
                find_one_key = get_choice()
                if find_one_key == '1':
                    mypkg.book.find_one_byISBN(book_list)
                elif find_one_key == '2':
                    mypkg.book.find_one_byname(book_list)
                elif find_one_key == '3':
                    mypkg.book.find_one_byauthor(book_list)
        elif key == '4':
            mypkg.menu.display_borrow_menu()
            borrow_key = get_choice()
            if borrow_key == '1':
                mypkg.customer.inner_borrow_book(customer_list, book_list)
            elif borrow_key == '2':
                mypkg.customer.outer_borrow_book(customer_list, book_list)
        elif key == '5':
            mypkg.menu.display_return_menu()
            return_key = get_choice()
            if return_key == '1':
                mypkg.customer.inner_return_book(customer_list, book_list)
            elif return_key == '2':
                mypkg.customer.outer_return_book(customer_list, book_list)
        elif key == '6':
            exit_name = False
        else:
            print("请输入正确的数值！")


if __name__ == '__main__':
    main()