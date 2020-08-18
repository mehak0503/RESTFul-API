import twint
import datetime
from elasticsearch import Elasticsearch
import json,requests
from bs4 import BeautifulSoup
from newspaper import Article
import hashlib

#Elasticsearch connection
def es_connect():
    try:
        return Elasticsearch([{'host':'10.30.16.91','port':9200}])
    except:
        print("Failed to connect to elasticsearch")

#Store data in elasticsearch
def store_in_es(data,index):
    try:
        json_data = json.loads(data)
        es = es_connect()
        for i in json_data:
            es.index(index=index,ignore=400,body=json_data[i])
    except:
        print("Error in storing data in elasticsearch")

#Fetch tweets of past one month with a keyword
def twitter_crawler(keyword):
    try:
        today = datetime.date.today()
        lastMonth = today - datetime.timedelta(days=30)
        c = twint.Config()
        c.Search = keyword
        c.Since = lastMonth.strftime('%Y-%m-%d %H:%M:%S')
        c.Hide_output = True
        c.Pandas = True
        c.Limit = 10
        twint.run.Search(c)
        df = twint.storage.panda.Tweets_df
        store_in_es(df.to_json(orient='index'),'mtwitter')
    except:
        print("Error in twitter crawler")

#Fetch the articles and store filtered articles
def extract_store_news(links,keyword):
    try:
        data = []
        for url in links:
            article = Article(url)
            try:
                article.download()
                article.parse()
            except:
                continue
            if keyword in article.text.lower():
                item = {'url':url,'title':article.title.lower(),'author':article.authors,'text':article.text.lower(),'publish_date':article.publish_date}    
                data.append(item)
        es = es_connect()
        for item in data:
            qhash = hashlib.md5(item['title'].encode()).hexdigest()
            doc = {"id":qhash,"url":item["url"],"title":item["title"],"text":item["text"],
                "publish_date":item["publish_date"],"hashtags":""}
            res = es.index(index="news", body=doc)
    except:
        print("Error in fetch and store news")

#Fetch news urls
def news_crawler(keyword):
    try:
        baseurl = 'https://www.altnews.in/page/'
        links = []
        for i in range(1,2):
            url = baseurl+str(i)
            response = requests.get(url)
            soup = BeautifulSoup(response.text,'lxml')
            linktags = soup.findAll("h2", {"class": "entry-title h3"})
            for i in linktags:
                link=i.findAll("a")
                links.append(link[0]["href"])
        extract_store_news(links,keyword)
    except:
        print("Error in news crawler")

#Get news crawler data
def get_news_data(keyword):
    try:
        result=[]
        es = es_connect()
        dt=es.search(index='news', body={"query":{"match":{"text":str(input)}}})
        for i in dt['hits']['hits']:
            result.append(i['_source'])
        return result
    except:
        print("Error in get news")


#Get twitter crawler data
def get_twitter_data(keyword):
    try:
        result=[]
        es = es_connect()
        dt=es.search(index='mtwitter', body={"query":{"match":{"tweet":str(keyword)}}})
        for i in dt['hits']['hits']:
            result.append(i['_source'])
        return result
    except:
        print("Error in get twitter data")