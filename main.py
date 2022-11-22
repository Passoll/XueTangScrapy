# Author Ayyyse--passo

import requests
import json
import re
import time

#-------------Please fill below

# https://www.xuetangx.com/learn/thu08281002136/thu08281002136/12424683/video/23293273
# https://www.xuetangx.com/learn/THU00001001632/THU00001001632/12423821/exercise/23218549
# Any page related to the class
url_page = 'https://www.xuetangx.com/learn/thu08281002136/thu08281002136/12424683/video/23293273'
# your own cookie
cookies = ''
out_name = 'test.json'

#-------------


headers = {
    'authority': 'www.xuetangx.com',
    'accept': 'application/json, text/plain, */*',
    'django-language': 'zh',
    'x-client': 'web',
    'accept-language': 'zh',
    'xtbz': 'xt',
    'user-agent': 'jdapp;android;8.4.2;8.0.0;;network/wifi;model/Mi Note 2;osVer/26;appBuild/71043;psn/|7;psq/1;uid/;adk/;ads/;pap/JA2015_311210|8.4.2|ANDROID 8.0.0;osv/8.0.0;pv/2.23;jdv/;ref/com.jingdong.app.mall.WebActivity;partner/huawei;apprpd/Home_Main;Mozilla/5.0 (Linux; Android 8.0.0; Mi Note 2 Build/OPR1.170623.032; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.99 Mobile Safari/537.36',
    'x-csrftoken': 'undefined',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.xuetangx.com/learn/',
    'cookie': cookies,
}

pat = re.compile('[^/]+')
cid = re.findall(pat,url_page)[5]
sign = re.findall(pat,url_page)[4]

params = (
    ('cid', cid),
    ('sign', sign),
)

response = requests.get('https://www.xuetangx.com/api/v1/lms/learn/course/chapter', headers=headers, params=params)
leafdict = json.loads(response.text)

if (response):
    print("success")
search_list = {}
chap_list = leafdict['data']['course_chapter']
for i in chap_list:
    section_list = i['section_leaf_list']

    #sec is a list with dic
    for section in section_list:
        if 'leaf_list' in section.keys():
            leaf_list = section["leaf_list"]
            for leaf_list_sub in leaf_list:
                search_list[leaf_list_sub['name']] = leaf_list_sub['id']
print(search_list)
# find the caption ?sign=thu08281005611 23431437
out = {}
for key,value in search_list.items():
    #sleep a while
    time.sleep(0.5)
    url_cap = 'https://www.xuetangx.com/api/v1/lms/learn/leaf_info/' + str(cid) + '/' + str(value) + '/?sign=' + str(sign)
    response = requests.get(url_cap, headers=headers)
    capdict = response.json()
    text = capdict['data']['content_info']['media']['ccid'] + '&lg=0'
    print(text)
    url = 'https://www.xuetangx.com/api/v1/lms/service/subtitle_parse/?c_d=' + text
    response2 = requests.get(url, headers=headers)
    out[key] = response2.json()['text']

with open(out_name, "w",encoding='utf-8') as f:
    json.dump(out, f, indent=4, ensure_ascii=False)
print(out)
print(‘success!’)
