import requests
import re
from bs4 import BeautifulSoup
import json

news_list = []
start = 1
end = 5
pages = list(range(start, end + 1))

for num in pages:
    url = f"http://www.econoi.com/news/articleList.html?page={num}&total=928&box_idxno=&sc_section_code=S1N1&view_type=sm"
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, "html.parser")
    news_list += ["http://www.econoi.com" + p.get("href") for p in soup.select("h4 > a")][:20]

data = []
for news in news_list:
    json_data = {}
    # sub crawling
    sub_req = requests.get(news)
    sub_html = sub_req.text
    sub_soup = BeautifulSoup(sub_html, "html.parser")

    # url
    json_data["url"] = news

    # title
    title = sub_soup.select_one(".heading").text
    json_data["title"] = title

    # sub_title
    if sub_soup.select_one(".subheading"):
        sub_title = sub_soup.select_one(".subheading").text
    else:
        sub_title = "null"
    json_data["sub_title"] = sub_title

    # author
    # date
    info = sub_soup.select(".infomation > li")
    info = [i.text.strip() for i in info][:-1]

    author = re.sub("[기자명|\\r|\\n|\\t]", "", info[0]).strip()
    date = re.sub("[가-힣]", "", info[-1]).strip()

    json_data["author"] = author
    json_data["date"] = date

    # article
    article = sub_soup.select("p")
    article = [re.sub("[\xa0\u200b\n\r\t]", "", p.text).strip() for p in article]
    article = " ".join(article)
    json_data["article"] = article

    # img_path
    if sub_soup.select("figure"):
        img_path = sub_soup.select_one("figure").img.get("src")
    else:
        img_path = "null"
    json_data["img_path"] = img_path

    # source
    json_data["source"] = "어린이 경제신문"

    data.append(json_data)

check = data[77]
for key in check:
    print(f"{key}: {check[key][:70]}")

with open("./econoi.json", "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, ensure_ascii=False)