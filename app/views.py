import os
from flask import Flask, render_template, request, jsonify
from app import app, host, port, user, passwd, db
from app.helpers.database import con_db
import sys
import ast
import json
import re
from find_similarity3 import find_companies
from operator import itemgetter



# ROUTING/VIEW FUNCTIONS
@app.route('/')
@app.route('/index')
def index():
#testing cursor/SQLconnection here.
#    cur = conn.cursor()
#    cur.execute('SELECT * FROM Investor_comp;')
#    rs = []
#    for r in cur:
#      print r
#      rs.append(str(r))
#    cur.close()
#    return '\n'.join(rs)
    return render_template('index.html')

    
@app.route('/api/users/<investorname>')  #this seems to work
def users(investorname):
    conn = con_db("localhost", 3306, "root", "****", "Venturenetwork18")
    cur = conn.cursor()
    find_investorID = '''SELECT investor_id FROM Investors_info WHERE investor_name="%s";'''% investorname
    cur.execute(find_investorID)
    investorID = cur.fetchall()
    investorID = investorID[0][0]
    [res, score] = find_companies(investorID)
    res2 = []
    cur.close()
    cur = conn.cursor()
    for row in res:
        
            #Statement = '''SELECT startup_name, startup_market, logolink, startupSignal FROM Starup_info WHERE startupID="%s";'''% row[1]
        Statement = '''SELECT startup_name, startup_market, logolink, startupSignal, angellink, funding, founder FROM Starup_info WHERE startupID="%s";'''% row[1]
        cur.execute(Statement)
        tmp = cur.fetchall()
        Statement2 = '''SELECT investor_id FROM Investor_comp WHERE startupID="%s";'''% row[1]
        cur.execute(Statement2)
        siminvestor_id = cur.fetchall()
        siminvestor = []
        for row2 in siminvestor_id: 
            for scoretmp in score:
                if row2 == scoretmp['investor_id']:
                    Statement3 = '''SELECT investor_name FROM Investors_info WHERE investor_id="%s";'''% scoretmp['investor_id']
                    cur.execute(Statement3)
                    siminvestor_name = cur.fetchall()[0][0]
                    siminvestor.append({'investor_name': siminvestor_name.decode('Windows-1252'), 'investor_score': scoretmp['similarity']})
        
        fund = 0;
        if len(tmp) > 0 and len(tmp[0][1]) > 2:
            fund = '{0:.2g}'.format(tmp[0][5])
            if float(fund) < 0.01:
                fund = 'N/A'
            else:
                fund = '$'+str(fund)+'M'
        if len(tmp) > 0:
            res2.append({'startup_score': row[0], 'startup_id': row[1],'startup_name': tmp[0][0].decode('Windows-1252'), 'startup_market': tmp[0][1].decode('Windows-1252'),'logolink': tmp[0][2].decode('Windows-1252'),'startupSignal': tmp[0][3], 'angellink': tmp[0][4].decode('Windows-1252'), 'founder':tmp[0][6].decode('Windows-1252'), 'funding': fund, 'investors': sorted(siminvestor, key=itemgetter('investor_score'),reverse=True)})  
    cur.close()
    return json.dumps(res2)
    #return json.dumps(len(tmp))
    #return json.dumps(tmp)


@app.route('/api/users_test2')
def users_test2():

    return render_template('users_test2.html')

@app.route('/api/users_test3')
def users_test3():

    return render_template('users_test3.html')

@app.route('/api/users_test4')
def users_test4():
    x = 1
    return render_template('users_test4.html', x = x)
    return render_template('users_test4.html')

@app.route('/api/w3school')
def w3school():

    return render_template('w3school.html')

@app.route('/home')
def home():
    # Renders home.html.
    return render_template('home.html')

@app.route('/slides')
def about():
    # Renders slides.html.
    return render_template('slides.html')

@app.route('/author')
def contact():
    # Renders author.html.
    return render_template('author.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500
