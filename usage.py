import requests,json

#POST request on news
def post_req_news(keyword):
    try:
        headers = {'Content-Type': 'application/json',}
        request = json.dumps({'keyword':keyword})
        response = requests.post('http://127.0.0.1:5000/news/', headers=headers, data=request)
        return response
    except:
        print("Error in POST news request")

#GET request on news
def get_req_news(keyword):
    try:
        headers = {'Content-Type': 'application/json',}
        request = {'keyword':keyword}
        response = requests.get('http://127.0.0.1:5000/news_data', headers=headers, data=request)
        return response
    except:
        print("Error in GET news request")

#POST request on twitter
def post_req_twitter(keyword):
    try:
        headers = {'Content-Type': 'application/json',}
        request = json.dumps({'keyword':keyword})
        response = requests.post('http://127.0.0.1:5000/twitter/', headers=headers, data=request)
        return response
    except:
        print("Error in POST twitter request")

#GET request on twitter
def get_req_twitter(keyword):
    try:
        headers = {'Content-Type': 'application/json',}
        request = {'keyword':keyword}
        response = requests.get('http://127.0.0.1:5000/twitter_data', headers=headers, params=request)
        return response
    except:
        print("Error in GET twitter request")