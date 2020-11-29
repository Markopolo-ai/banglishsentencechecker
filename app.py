# -*- coding: utf-8 -*-
"""
Created on thursday september 24 04:39:33 2020

@author: MOBASSIR
"""
from flask import Flask, render_template, url_for, request
import pandas as pd
import Levenshtein as lev
import re

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/predict',methods=['GET','POST'])
def predict():

    fullbanglaBanglish = pd.read_csv('Full_Bangla-Banglish.csv')
    fullbanglaBanglish = fullbanglaBanglish.drop(13094)
    benn = []
    romanicBanglaLyrics = "RomanicBanglaSongsLyrics.txt"
    
    #https://stackoverflow.com/questions/42339876/error-unicodedecodeerror-utf-8-codec-cant-decode-byte-0xff-in-position-0-in

    #with open(path , "rb") as f: # encoding = 'utf-8'
    with open(romanicBanglaLyrics, encoding="utf8", errors='ignore') as f:
        text = f.read()
    
    text2 = re.sub(r'[^a-z ]+', '', text.lower().replace('\n', ' '))

    for i  in range(len(text2)):
        data = text2[i].rstrip("\n")
        data = data.split('\t')
        benn.append(data[0])



    fullbanglaBanglish = fullbanglaBanglish.banglish.tolist()
    fullbanglaBanglish = [x for x in fullbanglaBanglish if str(x) != 'nan']
    fullbanglaBanglish = " ".join(fullbanglaBanglish)
    benn = " ".join(benn)
    banglishDictionary = fullbanglaBanglish + benn
    


    if request.method == 'POST':
            comment = request.form['comment']
            data = comment #[comment]

            def getMatch(string1,string2):
                min_sim = .70
                output = []
                res = [[lev.jaro_winkler(x,y) for x in string1.split()] for y in string2.split()]

                for x in res:
                    if max(x) >= min_sim:
                        output.append(string1.split()[x.index(max(x))])
                return output
            prediction = getMatch(banglishDictionary,data)
            prediction = " ".join(prediction)
           


    return render_template('result.html', prediction=prediction)


if __name__ == '__main__':
    app.run(debug=1,use_reloader=0, port=33507) #use_reloader=0,


