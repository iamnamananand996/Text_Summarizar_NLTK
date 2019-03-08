from flask import Flask,url_for,request, render_template
from flask_bootstrap import Bootstrap

from textSummary import nltk_summarizer
from nltk.tokenize import word_tokenize

import bs4
import requests


app = Flask(__name__)
Bootstrap(app)


# Scrap text
def url_text(url):
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text,'lxml')
    fetched_text = ' '.join(map(lambda p:p.text,soup.find_all('p')))
    return fetched_text



# Reading Time
def readingTime(mytext):
	total_words = len(word_tokenize(mytext))
	estimatedTime = total_words/200.0
	return estimatedTime




@app.route('/')
def main():
    return render_template("index.html")


@app.route('/summary',methods=['POST'])
def summary():

    if request.method == 'POST':
        data = request.form['data']
        data_time = readingTime(data)
        summaried_text = nltk_summarizer(data)
        summaried_text_time = readingTime(summaried_text)
        




    return render_template("index.html",raw_data=data,raw_data_len=len(data),data_time=data_time,summary=summaried_text,summary_len=len(summaried_text),summaried_text_time=summaried_text_time)



@app.route('/url_summary',methods=['POST'])
def url_summary():
    if request.method == 'POST':
        url = request.form['url']
        data = url_text(url)
        data_time = readingTime(data)
        summaried_text = nltk_summarizer(data)
        summaried_text_time = readingTime(summaried_text)
    

    return render_template("index.html",raw_data=data,raw_data_len=len(data),data_time=data_time,summary=summaried_text,summary_len=len(summaried_text),summaried_text_time=summaried_text_time)


if __name__ == "__main__":
    app.run(debug=True)