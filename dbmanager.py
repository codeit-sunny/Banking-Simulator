import sqlite3

def open_account(name, pwd, bal, mob, adhar, email, opendate):
    conobj = sqlite3.connect(database="bank.sqlite")
    curobj = conobj.cursor()

    query = "insert into accounts values(null,?,?,?,?,?,?,?)"
    curobj.execute(query, (name, pwd, bal, mob, adhar, email, opendate))

    acn = curobj.lastrowid

    conobj.commit()
    conobj.close()

    return acn


def login_account(uacn, upass):
    conobj = sqlite3.connect(database="bank.sqlite")
    curobj = conobj.cursor()

    query = "select * from accounts where acn=? and pass=?"
    curobj.execute(query, (uacn, upass))

    tup = curobj.fetchone()

    conobj.close()

    return tup


def get_account(uacn):
    conobj = sqlite3.connect(database="bank.sqlite")
    curobj = conobj.cursor()

    query = "select * from accounts where acn=?"
    curobj.execute(query, (uacn,))

    tup = curobj.fetchone()

    conobj.close()

    return tup


def get_name(uacn):
    conobj = sqlite3.connect(database="bank.sqlite")
    curobj = conobj.cursor()

    query = "select name from accounts where acn=?"
    curobj.execute(query, (uacn,))

    name = curobj.fetchone()[0]

    conobj.close()

    return name


def get_name_email(uacn):
    conobj = sqlite3.connect(database="bank.sqlite")
    curobj = conobj.cursor()

    query = "select name,email from accounts where acn=?"
    curobj.execute(query, (uacn,))

    tup = curobj.fetchone()

    conobj.close()

    return tup


def delete_account(uacn):
    conobj = sqlite3.connect(database="bank.sqlite")
    curobj = conobj.cursor()

    query = "delete from accounts where acn=?"
    curobj.execute(query, (uacn,))

    conobj.commit()
    conobj.close()


def get_balance(uacn):
    conobj = sqlite3.connect(database="bank.sqlite")
    curobj = conobj.cursor()

    query = "select bal from accounts where acn=?"
    curobj.execute(query, (uacn,))

    bal = curobj.fetchone()[0]

    conobj.close()

    return bal


def deposit_amount(uacn, uamt):
    conobj = sqlite3.connect(database="bank.sqlite")
    curobj = conobj.cursor()

    query = "update accounts set bal=bal+? where acn=?"
    curobj.execute(query, (uamt, uacn))

    conobj.commit()
    conobj.close()


def withdraw_amount(uacn, uamt):
    conobj = sqlite3.connect(database="bank.sqlite")
    curobj = conobj.cursor()

    query = "update accounts set bal=bal-? where acn=?"
    curobj.execute(query, (uamt, uacn))

    conobj.commit()
    conobj.close()


def transfer_amount(uacn, toacn, uamt):
    conobj = sqlite3.connect(database="bank.sqlite")
    curobj = conobj.cursor()

    query1 = "update accounts set bal=bal-? where acn=?"
    query2 = "update accounts set bal=bal+? where acn=?"

    curobj.execute(query1, (uamt, uacn))
    curobj.execute(query2, (uamt, toacn))

    conobj.commit()
    conobj.close()