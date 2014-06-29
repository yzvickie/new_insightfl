import sys
import string
import requests
import json
import pymysql 

def create_db(host, user, passwd):

    #con = pymysql.connect(host='localhost', user=user, passwd=passwd)
    con = pymysql.connect(host='localhost', user='root', passwd='****')
    cur = con.cursor()
    cur.execute('''DROP DATABASE if exists Venturenetwork18;''')
    cur.execute('''CREATE DATABASE Venturenetwork18;''')
    cur.execute('''USE Venturenetwork18;''')
    cur.execute('''CREATE TABLE Investor_comp (
                     investor_id int NOT NULL, 
                     startupID int

                   );''')
    
    cur.execute(''' CREATE TABLE Investors_info (
                    investor_id int NOT NULL, 
                    investor_name TEXT,
                    investor_score TEXT,

                    PRIMARY KEY (investor_id)
                    );''')
    
    cur.execute(''' CREATE TABLE Starup_info (
                    startupID int NOT NULL, 
                    startup_name TEXT,
                    startup_market TEXT,
                    founder TEXT,
                    startupSignal int,
                    angellink TEXT,
                    logolink TEXT,
                    funding float,
                    startup_desc TEXT,

                    PRIMARY KEY (startupID)
                    )CHARSET='utf8';''')
    cur.close()
    con.close()

def insertdata_db(host, user, passwd):
    Investor_comp_pairs = open('invest_startup')
    investor_comp = json.load(Investor_comp_pairs)
    investorInfo2 = open('investorInfo2')
    investorInfo2 = json.load(investorInfo2)
    startup_info = open('startupinfo_list_markets_funding_founder')
    startup_info = json.load(startup_info)

    con = pymysql.connect(host='localhost', user='root', passwd='1234', charset='utf8')
    cur = con.cursor()
    for row in investor_comp:
        try:
            cur.execute('''USE Venturenetwork18;''')
            cur.execute('''INSERT INTO Investor_comp
                   VALUES (%s, %s)''', (row[0], row[1]))
        except Exception, e:
            print row, e

    for row in investorInfo2:
        try:
            cur.execute('''USE Venturenetwork18;''')
            cur.execute('''INSERT INTO Investors_info
                   VALUES (%s, %s, %s)''', (row['userID'], row['name'], row['userscore']))
        except Exception, e:
            print row, e
    
    for row in startup_info:
        try:
            cur.execute('''USE Venturenetwork18;''')
            cur.execute('''INSERT INTO Starup_info
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''', (row['id'], row['name'], row['market'], row['founder'], row['quality'], row['angellist_url'], row['logo_url'],row['totalfunding'], row['product_desc']))
        except Exception, e:
            print row, e

    cur.close()
    con.commit()
    con.close()
    
def query_db(host, user, passwd):
    
    con = pymysql.connect(host='localhost', user='root', passwd='1234')
    cur = con.cursor()
    cur.execute('''USE Venturenetwork18;''')
    cur.execute('''SELECT * FROM Starup_info''')
    for i in cur:
        print i

    cur.close()
    con.commit()
    con.close()
create_db('localhost', 'root', '1234')
insertdata_db('localhost', 'root', '1234')
query_db('localhost', 'root', '1234')