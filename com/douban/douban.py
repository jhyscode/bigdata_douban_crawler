import requests
from bs4 import BeautifulSoup
import lxml
import json
import re
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
        json_str = json.loads(singlePage_jsonList,encoding='utf-8')['data']  #将一个JSON编码的字符串转换回一个Python数据结构字典
        json_str_list = list(json_str)
        #print(len(json_str_list))
        for item in json_str_list: #获取每页20个电影的ID
            movie_ids.append(item['id'])

        for id in movie_ids:
            movie_url = movieItem_baseUrl + str(id)+"/comments?status=P" #实际的电影评论的url地址
            movie_response = requests.get(movie_url, headers=headers)
            movie_soup = BeautifulSoup(movie_response.text, 'lxml')
            comment_list = movie_soup.find_all('div',class_='comment') #获取单个电影的首页评论列表

            for item in comment_list:
                try:
                    movie = {}
                    movie['name'] = movie_soup.find(id="content").h1.get_text()[0:-2]  # 获取电影标题
                    #print(movie['name'])
                    movie['comment_content'] = item.find('span', class_='short').get_text()  # 获取评论实体
                    movie['comment_star'] = \
                    item.find('span', class_='comment-info').find('span', {'class': re.compile("allstar")}).get(
                        'class')[0][-2:-1]  # 获取评论星级
                    movie['comment_id'] = item.find('span', class_='comment-info').find('a').get_text() #获取评论者ID
                    movie['comment_time'] = item.find('span', class_='comment-info').find('span',class_="comment-time").get_text() #获取评论时间
                    movie['comment_votes'] = item.find('span',class_='votes').get_text() #获取评论点赞数
                    print(movie)
                except:
                    print("")

if __name__ == '__main__':
    get_list()