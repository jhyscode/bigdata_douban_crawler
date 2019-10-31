import requests
from bs4 import BeautifulSoup
import lxml
import json
import re
import pymysql
import time

def get_list():
    #定义请求头
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 6.1;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 45.0.2454.101Safari / 537.36'
    }

    movieItem_baseUrl = "https://movie.douban.com/subject/"
    base_url = "https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=%E5%8A%A8%E6%BC%AB&start="
    for i in range(0,450):  #爬取前450页列表页的所有数据
        req = base_url + str(i*20)
        movie_ids = []
        response = requests.get(req, headers = headers)
        soup = BeautifulSoup(response.text,'lxml')
        singlePage_jsonList = soup.find('p').text  #返回的response为json字符串
        json_str = json.loads(singlePage_jsonList,encoding='utf-8')['data']  #将一个JSON编码的字符串转换回一个Python数据结构字典
        json_str_list = list(json_str)

        for item in json_str_list: #获取每页20个电影的ID
            movie_ids.append(item['id'])

        for id in movie_ids:
            time.sleep(0.5)  #设置单个电影页面的爬取时间间隔为0.5s，避免IP被封
            movie_url = movieItem_baseUrl + str(id)+"/comments?status=P" #实际的电影评论的url地址
            movie_response = requests.get(movie_url, headers=headers)
            movie_soup = BeautifulSoup(movie_response.text, 'lxml')
            comment_list = movie_soup.find_all('div',class_='comment') #获取单个电影的首页评论列表
            lists = []  # 存放每条评论的列表
            for item in comment_list:
                    movie = {}
                    movie['name'] = movie_soup.find(id="content").h1.get_text()[0:-2]  # 获取电影标题
                    try:
                        movie['comment_content'] = item.find('span', class_='short').get_text() # 获取评论实体
                    except:
                        movie['comment_content'] = ""
                    try:
                        movie['comment_star'] = \
                            item.find('span', class_='comment-info').find('span', {'class': re.compile("allstar")}).get(
                                'class')[0][-2:-1]  # 获取评论星级
                    except:
                        movie['comment_star'] = ""
                    try:
                        movie['comment_id'] = item.find('span', class_='comment-info').find('a').get_text()  # 获取评论者ID
                    except:
                        movie['comment_id'] = ""
                    try:
                        movie['comment_time'] = item.find('span', class_='comment-info').find('span',
                                                                                              class_="comment-time").get_text()  # 获取评论时间
                    except:
                        movie['comment_time'] = ""
                    try:
                        movie['comment_votes'] = item.find('span', class_='votes').get_text()  # 获取评论点赞数
                    except:
                        movie['comment_votes'] = ""
                    #写入数据库部分
                    db = pymysql.connect("localhost", "root", "199505", "douban_crawler")
                    cursor = db.cursor()
                    table = 'douban'
                    keys = ', '.join(movie.keys())
                    values = ', '.join(['%s'] * len(movie))
                    sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
                    try:
                        if cursor.execute(sql, tuple(movie.values())):
                            print('Successful')
                            db.commit()
                    except:
                        print('Failed')
                        db.rollback()
                    db.close()
                    #insert_sql( movie['name'],movie['comment_content'],)

if __name__ == '__main__':
    get_list()