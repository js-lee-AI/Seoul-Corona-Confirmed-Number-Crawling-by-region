# !pip install -U selenium
# !pip install beautifulsoup4
# !pip install pandas

# 크롤링 작업을 위한 라이브러리 임포트
import os
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
# import time

def remove_tag(content):
    tags = re.sub('<.+?>', ' ', content, 0, re.I|re.S)
    tags = tags.replace('(', '').replace(')', '')
    return tags

req = requests.get("http://www.seoul.go.kr/coronaV/coronaStatus.do?tab=1")

html = req.text
soup = BeautifulSoup(html, "html.parser")

total_num = remove_tag(str(soup.select(\
        "#tab-cont1 > div > div.status > div.status-seoul > div.cell-group.first-cell > div.cell.cell1 > div > p.counter")))
total_num = int(str(total_num).replace('[', '').replace(']', ''))

max_pages = total_num // 100 + 2  # 한 페이지당 100명까지 채워놓음.

result = []

for pages in range(1, max_pages):
    print("데이터 수집중... {}%".format(int(100*pages/max_pages)))
    for lists in range(1, 101):
        if soup.select("#cont-page{} > table > tbody > tr:nth-child({})" \
                               .format(pages, lists)) == []:
            break
        else:
            result.append(soup.select("#cont-page{} > table > tbody > tr:nth-child({})" \
                                      .format(pages, lists)))

results = []

for i in range(0, len(result)):
    results.append(remove_tag(str(result[i][0])).replace('  ', '\t'))

total = []
for i in range(len(results)):
    total.append(results[i].split('\t'))
    total[i].pop(0)
    total[i].pop(-1)
    total[i][0] = int(total[i][0])

total.sort(reverse=True)
# print(total)

df = pd.DataFrame(total)

header_ = pd.DataFrame([['서울 연번', '환자 번호', '확진일자', '성별, 출생년도', '거주지', '여행국',
        '접촉 환자', '조치사항']])
header_.to_csv('seoul_confimed.csv', index=False, mode='w', encoding='utf-8-sig',
              header=False)
df.to_csv('seoul_confimed.csv', index=False, mode='a', encoding='utf-8-sig',
         header=False)

print("\nCSV 파일 저장 완료")