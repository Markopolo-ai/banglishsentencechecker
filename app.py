# -*- coding: utf-8 -*-
"""
Created on thursday september 24 04:39:33 2020

@author: MOBASSIR
"""
from flask import Flask, render_template, url_for, request
import pandas as pd
import Levenshtein as lev

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/predict',methods=['GET','POST'])
def predict():
        fullbanglaBanglish = pd.read_csv('Full_Bangla-Banglish.csv')
        fullbanglaBanglish = fullbanglaBanglish.drop(13094)
        benn = []
        zamanbhaiBanglish = "banglish_zamanBhaiCorpus.txt"
        text_file = open(zamanbhaiBanglish, "r")
        lines = text_file.readlines()
        for i  in range(len(lines)):
                data = lines[i].rstrip("\n")
                data = data.split('\t')
                benn.append(data[0])
        text_file.close()

        fullbanglaBanglish = fullbanglaBanglish.banglish.tolist()
        fullbanglaBanglish = [x for x in fullbanglaBanglish if str(x) != 'nan']
        fullbanglaBanglish = " ".join(fullbanglaBanglish)
        benn = " ".join(benn)
        banglishDictionary = fullbanglaBanglish + benn
        


        if request.method == 'POST':
                comment = request.form['comment']
                data = comment #[comment]

                def getMatch(string1,string2):
                    min_sim = .80
                    output = []
                    res = [[lev.jaro_winkler(x,y) for x in string1.split()] for y in string2.split()]
                    print(res)
                    for x in res:
                        if max(x) >= min_sim:
                            output.append(string1.split()[x.index(max(x))])
                    return output
                prediction = getMatch(banglishDictionary,data)
                prediction = " ".join(prediction)
               


        return render_template('result.html', prediction=prediction)


if __name__ == '__main__':
    app.run(debug=True, port=33507)


