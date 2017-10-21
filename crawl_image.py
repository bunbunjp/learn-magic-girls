#!/usr/local/bin/python3
# vim: set fileencoding=UTF-8:

import os.path
import shutil
import urllib
import argparse
import requests
from analysis_images import ImageConsts


def url2file_name(url):
    """
    urlからファイル名を抜き取る
    :param url:
    :return filename: ファイル名文字列
    """
    return url.rsplit('/', 1)[1].split('?')[0]


def download_image(url, file_name, category):
    """
    url指定した画像をcategoryディレクトリにfile_nameで保存します。
    :param url:
    :param file_name:
    :param category:
    :return:
    """
    file_req = requests.get(url=url, stream=True)
    dir_path = './images/{0}'.format(category)
    file_path = '{1}/{0}'.format(file_name, dir_path)

    if not os.path.isdir(dir_path):
        os.makedirs(dir_path, exist_ok=True)

    with open(file=file_path, mode='wb') as fp:
        shutil.copyfileobj(file_req.raw, fp)


def create_query_url(query, count, api_key, search_engine_key):
    """
    画像検索を実行するURLを返却します
    :param query:
    :param count:
    :param api_key:
    :param search_engine_key:
    :return url_string:
    """
    q = urllib.parse.quote(query)
    return 'https://www.googleapis.com/customsearch/v1?key={2}&cx={3}&q={0}&searchType=image&imgType=face&start={1}'.format(q, str(count), api_key, search_engine_key)



if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--api_key', default=None, required=True)
    argparser.add_argument('--search_engine_key', default=None, required=True)

    args = argparser.parse_args()
    api_key = args.api_key
    search_engine_key = args.search_engine_key

    targets = ImageConsts.CATEGORIES
    for t in targets:
        print(t)
        for i in range(1, 6):
            requesturl = create_query_url(query=t,
                                          count=i*10,
                                          api_key=api_key,
                                          search_engine_key=search_engine_key)
            response = requests.get(requesturl)
            print(response.text)
            json_data = response.json()
            items = json_data['items']

            for item in items:
                url = item['link']
                file_name = url2file_name(url)

                if not file_name or not url:
                    continue

                download_image(url=url, file_name=file_name, category=t)

