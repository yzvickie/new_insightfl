import sys
import string
import requests
import json
import pymysql 
import numpy as np
import pandas as pd
from operator import itemgetter
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA, RandomizedPCA, TruncatedSVD
from sklearn.preprocessing import Normalizer

def find_companies(investorname):
    investorname = np.int(investorname)
    rmatrix= np.loadtxt(open("investorcompanyPCA.csv"),delimiter=",")
    investor_id = np.loadtxt(open("investorIDorder.csv"),delimiter=",")
    investor_id = investor_id.astype(int)
    count=0
    score = []
    target=[]
    for row in investor_id:
        if row == investorname:
            target = rmatrix[count]
            break
        count += 1
    
    counter2 = 0
    for row in rmatrix:
        #score.append([cosine_similarity(target,row).tolist()[0][0], investor_id[counter2]])
        score.append({u'similarity': cosine_similarity(target,row).tolist()[0][0], u'investor_id': investor_id[counter2]})
        counter2 += 1
    #score = sorted(score,reverse=True)
    con = pymysql.connect(host='localhost', user='root', passwd='1234')
    cur = con.cursor()
    cur.execute('''USE Venturenetwork16;''')
    current_query='''SELECT startupID FROM Investor_comp'''
    company_total = pd.io.sql.frame_query(current_query, con)
    company_total = list(company_total['startupID'])
    similarcomp=[]

    current_query='''SELECT * FROM Investor_comp'''
    rows = pd.io.sql.frame_query(current_query, con)
    df = pd.Series(list(rows['startupID']),list(rows['investor_id']))
    score = sorted(score,key=itemgetter('similarity'),reverse=True)
    similarcomp = []
    for investor_row in score[1:20]:
        for company in list(df[investor_row['investor_id']]):
            similarcomp.append([company, investor_row['similarity']])
    companyid = [ row[0] for row in similarcomp ]
    companysim = [ row[1] for row in similarcomp ]
    uniquecompID = list(set(companyid))
    uniquesimcomp = []
    for company in uniquecompID:
        compscore = 0
        for company2 in similarcomp:
            if company == company2[0] and company not in list(df[investorname]):
                compscore += company2[1]
        uniquesimcomp.append([compscore, company])
    return sorted(uniquesimcomp, reverse=True)[0:40], score   

if __name__ == "__main__":
    [uniquesimcomp,score] = find_companies(sys.argv[1])
    print [uniquesimcomp,score]
