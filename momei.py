#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import logging


def download_image(link, refere, folder):
    pass


def download_image(page, folder='images'):
    text = page
    # png 链接所在 id
    re_png_id = re.compile(r'(?i)<a\s+[^>]*?id="png"[^>]*>')
    # jpg 链接所在 id
    re_jpg_id = re.compile(r'(?i)<a\s+[^>]*?id="highres"[^>]*>')
    # 链接
    re_link = re.compile(r'(?i)href="([^"]+)"')
    png = re.findall(re_link, str(re.findall(re_png_id, text)))
    jpg = re.findall(re_link, str(re.findall(re_jpg_id, text)))
    logger2 = logging.getLogger('download_image')
    logger2.debug('png link: \n' + str(png))
    logger2.debug('jpg link: \n' + str(jpg))
    if png:
        return png[0]
    elif jpg:
        return jpg[0]
    else:
        return None


def get_image_pages(page):
    text = page
    # re_image = re.compile(r'''(?ix)<a\s[^>]*?class="thumb"[^>]*?href="([^"]+)"[^>]*?>''')
    # <span\s[^>]*?class="plid"[^>]*?>\s*\#pl\s+((?:https?://)?(?:[^/]*)?/[^\s<]+)[^<]*?</span>
    re_image = re.compile(r'''(?ix)<span\s[^>]*?class="plid"[^>]*?>
                          \s*\#pl\s+([^\s<]+)[^<]*?</span>''')
    re_next_a = re.compile(r'(?i)<a\s[^>]*?class="next_page"[^>]*>')
    re_next = re.compile(r'(?i)href="([^"]+)"')
    logger2 = logging.getLogger('get_image_pages')
    image_pages = re.findall(re_image, text)
    next_pages  = re.findall(re_next, str(re.findall(re_next_a, text)))
    logger2.debug('image pages: \n' + str(image_pages))
    logger2.debug('next page: ' + str(next_pages))
    next_page_ = next_pages[0] if next_pages else None
    image_pages_ = image_pages if image_pages else None
    return image_pages_, next_page_


if __name__ == '__main__':
    # import logging
    import charset
    logging.basicConfig(level=logging.DEBUG)
    # tag = raw_input(u'tag: ')
    # site = ''
    # query = 'https://yande.re/post?tags=kyubey'
    # 先通过request检测编码在使用 charset
    logger1 = logging.getLogger('__main__')
    logger1.debug('read file')
    with open(r'temp/227202.htm') as f:
        text1 = f.read()
        # logger.debug('file content\n' + repr(text1))
        text1 = charset.decode_(text1)
        # logger.debug('unicode file content\n' + repr(text1))
        logger1.debug('start download_image')
        image_link = download_image(text1)
        logger1.debug('return: ' + str(image_link))
    logger1.debug('read file')
    with open(r'temp/_kyubey.html') as f:
        text2 = f.read()
        # logger1.debug('file content\n' + repr(text2))
        text2 = charset.decode_(text2)
        # logger1.debug('unicode file content\n' + repr(text2))
        logger1.debug('start get_image_pages')
        image_link = get_image_pages(text2)
        logger1.debug('return:\n' + str(image_link))
