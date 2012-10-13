#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


def get_image_link(page):
    text = page
    # png 链接所在 id
    re_png_id = re.compile(r'(?i)<a\s+[^>]*?id="png"[^>]*>')
    # jpg 链接所在 id
    re_jpg_id = re.compile(r'(?i)<a\s+[^>]*?id="highres"[^>]*>')
    # 链接
    re_link = re.compile(r'(?i)href="([^"]+)"')
    png = re.findall(re_link, str(re.findall(re_png_id, text)))
    jpg = re.findall(re_link, str(re.findall(re_jpg_id, text)))
    if png:
        return png[0]
    elif jpg:
        return jpg[0]
    else:
        return None


def get_image_pages(page):
    """analysis page content.
    
    return (image_pages, next_page)
    
    images_pages is list
    
    next_page is string
    """
    text = page
    re_image = re.compile(r'''(?ix)<span\s[^>]*?class="plid"[^>]*?>
                          \s*\#pl\s+([^\s<]+)[^<]*?</span>''')
    re_next_a = re.compile(r'(?i)<a\s[^>]*?class="next_page"[^>]*>')
    re_next = re.compile(r'(?i)href="([^"]+)"')
    image_pages = re.findall(re_image, text)
    next_pages = re.findall(re_next, str(re.findall(re_next_a, text)))
    next_page_ = next_pages[0] if next_pages else None
    image_pages_ = image_pages if image_pages else None
    return image_pages_, next_page_

if __name__ == '__main__':
    import urllib2
    import time
    import copy
    import charset
    import requests
    # 获取输入的 tag，并按 utf8 编码
    tag = re.sub(r'\s+', '_', charset.decode_(raw_input(u'tag: ').strip())
                 ).encode('utf8')
    referer = site = 'https://yande.re/'
    # 配置 requests
    #payload = {'tags': tag}
    url = 'https://yande.re/post?tags=%s' % (urllib2.quote(tag))
    config = {'store_cookies' : False}
    headers = {
        'Host': 'yande.re',
        'User-Agent:': ('Mozilla/5.0 (Windows NT 6.2; rv:15.0) Gecko'
                        + '/20100101 Firefox/15.0.1'),
        'Connection': 'keep-alive',
        'Referer': referer
    }
    r = requests.get(url, headers=headers, params={},
                     config=config, prefetch=False)
    if r.status_code == requests.codes.ok:
        image_pages , next_page = get_image_pages(r.content)
        for i in image_pages:
            if not i.startswith('http'):
                i = site + i
        #if not next_page.startswith('http'):
        #    next_page += site
        for link in image_pages:
            r2 = requests.get(link, headers=headers,
                              config=config, prefetch=False)
            if r2.status_code == requests.codes.ok:
                image_link = get_image_link(r2.content)
                print image_link
                headers_ = copy.deepcopy(headers)
                headers_.update({'Referer': link})
                r3 = requests.get(image_link, headers=headers_,
                                  config=config, prefetch=False)
                if r3.status_code == requests.codes.ok:
                    file_name = urllib2.unquote(image_link.split('/')[-1])
                    with open(file_name, 'ab', buffering=0) as f:
                        for i in r3.iter_content(chunk_size=1*1024):
                            f.write(i)
                time.sleep(1*60)