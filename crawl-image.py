#!/usr/local/bin/python3
# vim: set fileencoding=UTF-8:

from PIL import Image
import numpy as np
import json, requests
import shutil, urllib, os.path, copy

api_key = "AIzaSyBkj0xZEJ4IQgSoplFkzH5DTQYgyTOccCw"
# api_key = "AIzaSyD8laRv_6fKzDsrnhUgFuoxKPtba3DXc_0"

search_engine_key = "013825985675592064113:kjv7zhv9pfc"
# search_engine_key = "007617141878436851031:ltnjz9szbky"

def url2file_name(url):
    return url.rsplit('/', 1)[1].split('?')[0]

def download_image(url, file_name, category):

    file_req = requests.get(url=url, stream=True)
    print(file_req.status_code)
    dir_path = './images/{0}'.format(category)
    file_path = '{1}/{0}'.format(file_name, dir_path)

    print('dir  : ', dir_path)
    print('file : ', file_path)
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path, exist_ok=True)

    with open(file=file_path, mode='wb') as fp:
        shutil.copyfileobj(file_req.raw, fp)

def create_query_url(query, count):
    q = urllib.parse.quote(query)
    return 'https://www.googleapis.com/customsearch/v1?key={2}&cx={3}&q={0}&searchType=image&imgType=face&start={1}'.format(q, str(count), api_key, search_engine_key)

#####
#
# https://www.googleapis.com/customsearch/v1?key=AIzaSyD8laRv_6fKzDsrnhUgFuoxKPtba3DXc_0&cx=007617141878436851031:o6jsofundn0&q=%E9%B9%BF%E7%9B%AE%E3%81%BE%E3%81%A9%E3%81%8B&searchType=image
#
#####

targets = ['鹿目まどか', '佐倉杏子', '美樹さやか', '巴まみ', '暁美ほむら']
for t in targets:
    print(t)
    for i in range(1, 6):
        response = requests.get(create_query_url(t, i*10))
        print(response.text)
        json_data = response.json()
        items = json_data['items']

        for item in items:
            url = item['link']
            file_name = url2file_name(url)

            if not file_name or not url:
                continue

            download_image(url=url, file_name=file_name, category=t)
exit()

