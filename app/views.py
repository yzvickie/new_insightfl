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

conn = con_db("localhost", 3306, "root", "1234", "Venturenetwork16")



# ROUTING/VIEW FUNCTIONS
@app.route('/')
@app.route('/index')
def index():
#testing cursor/SQLconnection here.
    cur = conn.cursor()
    cur.execute('SELECT * FROM Investor_comp;')
    rs = []
    for r in cur:
      print r
      rs.append(str(r))
    cur.close()
    return '\n'.join(rs)

    
@app.route('/api/users/<investorID>')  #this seems to work
def users(investorID):
    [res, score] = find_companies(investorID)
    res2 = []
    
    cur = conn.cursor()
    for row in res:
        #Statement = '''SELECT startup_name, startup_market, logolink, startupSignal FROM Starup_info WHERE startupID="%s";'''% row[1]
        Statement = '''SELECT startup_name, startup_market, logolink, startupSignal, angellink, funding FROM Starup_info WHERE startupID="%s";'''% row[1]
        cur.execute(Statement)
        tmp = cur.fetchall()
        Statement2 = '''SELECT investor_id FROM investor_comp WHERE startupID="%s";'''% row[1]
        cur.execute(Statement2)
        siminvestor_id = cur.fetchall()
        siminvestor = []
        for row2 in siminvestor_id: 
            for scoretmp in score:
                if row2 == scoretmp['investor_id']:
                    siminvestor.append({u'investor_id': scoretmp['investor_id'], u'investor_score': scoretmp['similarity']})
        

        if len(tmp) > 0 and len(tmp[0][1]) > 2:
            #tmp[0][5] = '{0:.2g}'.format(tmp[0][5])
            fund = '{0:.2g}'.format(tmp[0][5])
            if float(fund) < 0.01:
                fund = 'N/A'
            else:
                fund = '$'+str(fund)+'M'

            res2.append({u'startup_score': row[0], u'startup_id': row[1],u'startup_name': tmp[0][0], u'startup_market': tmp[0][1],u'logolink': tmp[0][2],u'startupSignal': tmp[0][3], u'angellink': tmp[0][4], u'funding': fund, u'investors': sorted(siminvestor, key=itemgetter('investor_score'),reverse=True)})  
    cur.close()
    return json.dumps(res2)
    #return json.dumps(result)


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
