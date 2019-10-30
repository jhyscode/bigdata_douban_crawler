import requests
from bs4 import BeautifulSoup
import lxml
import json
def get_list():
    #定义请求头
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 6.1;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 45.0.2454.101Safari / 537.36'
    }
    article_list = []
    movieItem_baseUrl = "https://movie.douban.com/subject/"
    base_url = "https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=%E5%8A%A8%E6%BC%AB&start="
    for i in range(0,1):
        req = base_url + str(i*20)
        movie_ids = []
        response = requests.get(req, headers = headers)
        soup = BeautifulSoup(response.text,'lxml')
        singlePage_jsonList = soup.find('p').text  #返回的response为json字符串
        json_str = json.loads(singlePage_jsonList,encoding='utf-8')['data']  #将一个JSON编码的字符串转换回一个Python数据结构
        json_str_list = list(json_str)
        #print(len(json_str_list))
        for item in json_str_list: #获取每页20个电影的ID
            movie_ids.append(item['id'])
        for id in movie_ids:
            movie_url = movieItem_baseUrl + str(id)+"/comments?status=P" #实际的电影评论的url地址
            movie_response = requests.get(movie_url,headers=headers)
            movie_soup = BeautifulSoup(movie_response.text,'lxml')
            


if __name__ == '__main__':
    get_list()