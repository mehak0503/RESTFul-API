from flask import Flask,render_template,request,jsonify
from utils import *
import ast
app = Flask(__name__) 
app.config["Debug"] = True


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/twitter/',methods=['POST'])
def twitter_data():
    try:
        dict_str = request.data.decode("UTF-8")
        data = ast.literal_eval(dict_str)
        keyword = data['keyword']
        if keyword:
            twitter_crawler(keyword)
            return render_template('twitter.html',key=keyword)
        else:
            return render_template('error.html')
    except:
        print("Error in fetching twitter data")


@app.route('/news/',methods=['POST'])
def news_data():
    try:
        dict_str = request.data.decode("UTF-8")
        data = ast.literal_eval(dict_str)
        keyword = data['keyword']
        if keyword:
            news_crawler(keyword)
            return render_template('news.html',key=keyword)
        else:
            return render_template('error.html')
    except:
        print("Error in fetching news data")

@app.route('/twitter_data',methods=['GET'])
def fetch_twitter_data():
    try:
        keyword = request.args.get('keyword')
        if keyword:
            data = get_twitter_data(keyword)
            return jsonify(data)
        else:
            return render_template('error.html')
    except:
        print("Error in fetching twitter data")


@app.route('/news_data',methods=['GET'])
def fetch_news_data():
    try:
        keyword = request.args.get('keyword')
        if keyword:
            data = get_news_data(keyword)
            return jsonify(data)
        else:
            return render_template('error.html')
    except:
        print("Error in fetching news data")

if __name__ == '__main__':
    app.run()