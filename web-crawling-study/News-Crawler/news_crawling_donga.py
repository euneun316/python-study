import requests
import re
# HTTP GET Request
## 어린이 동아 뉴스 리스트
req = requests.get("http://kids.donga.com/?ptype=article&psub=news")

html = req.text  # HTML (use this source!)
header = req.headers  # header
status = req.status_code  # status
is_ok = req.ok  # status boolean
print("done:", is_ok)
print("status:", status)
print("header:", header)

# !pip install bs4
from bs4 import BeautifulSoup

# convert HTML source to pythob object
## BeautifulSoup({html}, {parser})
soup = BeautifulSoup(html, "html.parser")

# CSS Selector
article_titles = soup.select("dt > a")
article_titles


# selector elements
print("text: ", article_titles[0].text)
print("href: ", article_titles[0].get("href"))


# title: body > div.wrap_all > div.content > div.page_area > div.at_cont > div.at_cont_title > div.at_info > ul > li.title
# author: body > div.wrap_all > div.content > div.page_area > div.at_cont > div.at_cont_title > div.at_info > ul > li.writer
# date: body > div.wrap_all > div.content > div.page_area > div.at_cont > div.at_cont_title > div.at_info > ul > li.upload_date
# article: body > div.wrap_all > div.content > div.page_area > div.at_cont > div.cont_view > div > p:nth - child(4) > span
# img_path: body > div.wrap_all > div.content > div.page_area > div.at_cont > div.cont_view > div > p:nth - child(1) > span > img

# sub crawling
href = article_titles[4].get("href")
sub_req = requests.get(href)
sub_html = sub_req.text
sub_soup = BeautifulSoup(sub_html, "html.parser")
# title

## title = sub_soup.select_one("li.title").text
title = "\xa02022 베이징 올림픽의 타임키퍼 ‘오메가’의 기술은? 생동감 넘치는 경기 전달해요!"  # 유니코드 공백문자
print("처리 전:", title)

## regex
pattern = re.compile("[\xa0\u200b\n\r\t]")  # regex 패턴 설정
title = re.sub(pattern, "", title)
print("처리 후:", title)

# author

## author = sub_soup.select_one("li.writer").text
writer = "\r\n\t\t\t\t\t김철수 기자\t\t\t\t\t"
print("처리 전:", writer)

writer = re.sub(pattern, "", writer.split(" ")[0])
print("처리 후:", writer)
# date
date = sub_soup.select_one("li.upload_date").text
date
'2022-02-02 12:47:00'
# article
article = sub_soup.select("div.at_content > p")  # 파싱
article = [
    p.text for p in article
    if not p.img  # img 태그 제거
    if not "위 기사의 법적인 책임과 권한은" in p.text  # 법적 고지 제거
    if not "< 저작권자 ⓒ 어린이동아" in p.text  # 법적 고지 제거
    if not ("▶어린이동아" and "기자") in p.text  # 기자 제거
]
article = " ".join(article)
article = re.sub(pattern, "", article)
article

# image path (두 가지 경우의 수)
try:
    img_path = sub_soup.select_one("div.at_content > p > img").get("src")
except:
    img_path = sub_soup.select_one("div.at_content > p > span > img").get("src")
img_path

# 크롤링 타겟 설정
# %%time
# news_titles = []
# pages = list(range(1, 11))

# for num in pages:
#     url = f"https://kids.donga.com/?page_no={num}&ptype=article&psub=news&gbn=01"
#     req = requests.get(url)
#     html = req.text
#     soup = BeautifulSoup(html, "html.parser")
#     news_titles += soup.select("dt > a")

# print("크롤링 타겟 수:", len(news_titles))


# %%time

num = 1
url = f"https://kids.donga.com/?page_no={num}&ptype=article&psub=news&gbn=01"
req = requests.get(url)
html = req.text
soup = BeautifulSoup(html, "html.parser")
news_titles = soup.select("dt > a")

print("크롤링 타겟 수:", len(news_titles))

# %%time

import requests
from bs4 import BeautifulSoup
import re

pattern = re.compile("[\xa0\u200b\n\r\t]")  # regex pattern
data = []
for title in news_titles:
    json_data = {}

    # sub crawling
    sub_url = title.get("href")
    sub_req = requests.get(sub_url)
    sub_html = sub_req.text
    sub_soup = BeautifulSoup(sub_html, "html.parser")

    # url
    json_data["url"] = sub_url

    # title
    title = sub_soup.select_one("li.title").text
    title = re.sub(pattern, "", title)
    json_data["title"] = title

    # author
    author = sub_soup.select_one("li.writer").text
    author = re.sub(pattern, "", author.split(" ")[0])
    json_data["author"] = author

    # date
    date = sub_soup.select_one("li.upload_date").text
    json_data["date"] = date

    # article
    article = sub_soup.select("div.at_content > p")
    article = [
        p.text for p in article
        if not p.img
        if not "위 기사의 법적인 책임과 권한은" in p.text
        if not "< 저작권자 ⓒ 어린이동아" in p.text
        if not ("▶어린이동아" and "기자") in p.text
    ]
    article = " ".join(article)
    article = re.sub(pattern, "", article)
    article
    json_data["article"] = article

    # img_path
    img_path = sub_soup.select_one("div.at_content img").get("src")
    json_data["img_path"] = img_path

    # source
    json_data["source"] = "어린이동아"

    data.append(json_data)
print("크롤링 데이터 수:", len(data))

data[:3]

data[1]["article"]

# json 파일로 저장
# import json
# with open("donga_crawling.json", "w", encoding="utf-8") as json_file:
#     json.dump(data, json_file,  ensure_ascii=False)

article_titles

from datetime import datetime

today = datetime.today().strftime("%Y%m%d")
today
'20220202'
today_article = [i for i in article_titles if today in i.get("href")]
today_article