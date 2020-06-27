drop database if exists `libmgmt`;
create database if not exists `libmgmt`;
use `libmgmt`;

create table books
(
    ISBN           char(15)     not null
        primary key,
    name           varchar(100) null,
    author         varchar(100) null,
    publisher      varchar(100) null,
    pubyear        year         null,
    classification int          null,
    num            int          null
);

create table customers
(
    id           int auto_increment
        primary key,
    name         varchar(100)  null comment '用户姓名',
    type         int           null comment '用户类型 0-外部 1-内部',
    borrowed_num int default 0 null comment '已借阅数'
);

create table inner_customers
(
    id   int          not null,
    code varchar(20)  not null comment '学号/工号'
        primary key,
    name varchar(100) null,
    constraint inner_customers_customers_id_fk
        foreign key (id) references customers (id)
);

create table outer_customers
(
    id   int          not null,
    code varchar(20)  not null comment '身份证号'
        primary key,
    name varchar(100) null,
    constraint outer_customers_customers_id_fk
        foreign key (id) references customers (id)
);

create table customer_book
(
    id   int      not null,
    ISBN char(15) not null,
    date date     not null,
    constraint customer_book_books_ISBN_fk
        foreign key (ISBN) references books (ISBN),
    constraint customer_book_customers_id_fk
        foreign key (id) references customers (id)
);
