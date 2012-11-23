#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


def get_image_link(page):
    """返回图片下载链接（字符串值或 None）

    page: 图片查看页面网页源代码
    """
    text = page
    # png 链接所在 id
    re_png_id = re.compile(r'(?i)<a\s+[^>]*?id="png"[^>]*>')
    # jpg 链接所在 id
    re_jpg_id = re.compile(r'(?i)<a\s+[^>]*?id="highres"[^>]*>')
    # 链接
    re_link = re.compile(r'(?i)href="([^"]+)"')
    png = re.findall(re_link, str(re.findall(re_png_id, text)))
    jpg = re.findall(re_link, str(re.findall(re_jpg_id, text)))
    # 优先获取 png 图片下载链接
    # 因为当存在 png 链接时，
    # 此时的 jpg 图片其实是经过 png >> jpg 转换的，
    # 失去了透明背景
    if png:
        return png[0]
    elif jpg:
        return jpg[0]
    else:
        return None


def get_image_pages(page):
    """分析搜索结果页面源代码，
    返回结果条目链接及下一页链接

    return image_pages, next_page
    images_pages：由搜索结果条目链接组成的列表，默认值为 None
    next_page：字符串，下一页链接，默认值为 None
    """
    text = page
    # 搜索结果条目链接
    re_image = re.compile(r'''(?ix)<span\s[^>]*?class="plid"[^>]*?>
                          \s*\#pl\s+([^\s<]+)[^<]*?</span>''')
    # 下一页所在 a 标签
    re_next_a = re.compile(r'(?i)<a\s[^>]*?class="next_page"[^>]*>')
    re_next = re.compile(r'(?i)href="([^"]+)"')
    image_pages = re.findall(re_image, text)
    next_pages = re.findall(re_next, str(re.findall(re_next_a, text)))
    next_page_ = next_pages[0] if next_pages else None
    image_pages_ = image_pages or None
    return image_pages_, next_page_

if __name__ == '__main__':
    # TODO momei.py max_i=18 max_n=1 save='image' proxy_t=http
    # proxy_s='127.0.0.1:7071' site='https://yande.re/' sleep=100
    # chunk_size=1000
    # agent='Mozilla/5.0 (Windows NT 6.2; rv:15.0) Gecko/20100101
    # Firefox/15.0.1'
    import urllib2
    import urlparse
    import time
    import os
    import charset
    # from optparse import OptionParser
    import requests
    # parser = OptionParser()
    save_path = 'images'
    # 如果路径不存在
    if not os.path.exists(save_path):
        # 创建用来保存图片的文件夹
        os.makedirs(save_path)
    # 获取输入的 tag，并按 utf8 编码
    tag = re.sub(r'\s+', '_', charset.decode_(raw_input(u'tag: ').strip())
                 ).encode('utf8')
    max_image_page = 18
    max_next_page = 1
    sleep = 0.5 * 60
    referer = site = 'https://yande.re/'
    # 配置 requests
    #payload = {'tags': tag}
    url = 'https://yande.re/post?tags=%s' % (urllib2.quote(tag))
    config = {'store_cookies': False}
    # proxies = {
        # 'http': '127.0.0.1:7071',
        # 'https': '127.0.0.1:8088',
        # 'http': 'http://user:pass@127.0.0.0.1:3021/',
    # }
    proxies = dict()
    # proxy_type = 'http'
    # proxy_site = '127.0.0.1:7071'
    # proxies.update({proxy_type: proxy_site})
    # 获取最新地址
    # referer = site = requests.get(site, config=config, proxies=proxies,
                                    # prefetch=False).url
    headers = {
        'Host': urlparse.urlsplit(site).netloc,
        'User-Agent': ('Mozilla/5.0 (Windows NT 6.2; rv:15.0) Gecko'
                       + '/20100101 Firefox/15.0.1'),
        'Connection': 'keep-alive',
        'Referer': referer
    }
    while max_next_page >= 0:
        # print url
        r = requests.get(url, headers=headers, params={},
                         config=config, proxies=proxies, prefetch=False)
        if r.status_code == requests.codes.ok:
            image_pages, next_page = get_image_pages(r.content)
            if not image_pages:
                print 'no image'
                break
            for i in image_pages:
                if not i.startswith('http'):
                    i = site + i
            for link in image_pages:
                if max_image_page == 0:
                    break
                referer = url
                headers.update({'Referer': referer})
                r2 = requests.get(link, headers=headers, proxies=proxies,
                                  config=config, prefetch=False)
                if r2.status_code == requests.codes.ok:
                    image_link = get_image_link(r2.content)
                    # print image_link
                    file_name = urllib2.unquote(image_link.split('/')[-1])
                    file_path = save_path + os.sep + file_name
                    if not os.path.exists(file_name):
                        referer = link
                        headers.update({'Referer': referer})
                        r3 = requests.get(image_link, headers=headers,
                                          proxies=proxies,
                                          config=config, prefetch=False)
                        # print r3.request.headers
                        if r3.status_code == requests.codes.ok:
                            with open(file_path, 'ab', buffering=0) as f:
                                for i in r3.iter_content(chunk_size=50 * 1024):
                                    f.write(i)
                        print u'Finished download %s !' % (image_link)
                max_image_page -= 1
                time.sleep(sleep)
            if next_page:
                if not next_page.startswith('http'):
                    next_page = site + next_page
                referer = url
                headers.update({'Referer': referer})
                url = next_page.replace('&amp;', '&')
                max_next_page -= 1
            else:
                break
        else:
            r.raise_for_status()
            break
    print 'finished'
