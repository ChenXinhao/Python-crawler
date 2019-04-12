# -*- coding: utf-8 -*-

import os
import sys
import time
import re

import requests
from bs4 import BeautifulSoup
import codecs
import pdb
from jiebao import ExtSougouScel
import codecs


class SogouSpider:
    def __init__(self):
        self.base_url = 'https://pinyin.sogou.com'
        self.file_count = 0
        self.name_set = set()

    def load_name(self, name_set):
        self.name_set = name_set
        self.file_count = len(name_set)

    def get_html_text(self, url):
        try:
            r = requests.get(url, timeout=15, stream=True)
            r.encoding = r.apparent_encoding
            return r.text
        except:
            print ('[error]get_html_text', url, 'fail')
            return -1

    def solve_dict_cate(self, url, index=1):
        print ('[in]' + url + '/default/' + str(index))
        html = self.get_html_text(url + '/default/' + str(index))
        soup = BeautifulSoup(html, 'lxml')
        end_flag = True
        for x in soup.findAll("div", {"class": "dict_detail_block"}):
            end_flag = False
            name = x.find("div", {"class": "detail_title"}).a.text.strip().replace('\x00', '')
            if name in self.name_set:
                continue
            print ('start solve ' + name)
            info = x.findAll("div", {"class": "show_content"})
            info_dict = {}
            info_dict['example'] = ' '.join(info[0].text.split('、'))
            info_dict['download_times'] = info[1].text
            info_dict['update_time'] = info[2].text
            info_dict['name'] = name
            dl_link = x.find("div", {"class": "dict_dl_btn"}).a['href']
            info_dict['link'] = dl_link
            try:
                print ('start download ')
                dl_r = requests.get(dl_link)
                scel_decode = ExtSougouScel()
                info_dict.update(scel_decode.deal_from_content(dl_r.content))
                f = codecs.open('new_data/' + str(self.file_count) + '.sogou_dict', 'w', 'utf-8')
                self.file_count += 1
                for k, v in info_dict.items():
                    f.write(k + '\t' + v + '\n')
            except:
                print ('[fail in]' + dl_link + '[name]' + name)
                continue

            print ('download ' + info_dict['name'] + 'done [', self.file_count, ' files done]')
        if not end_flag:
            self.solve_dict_cate(url, index + 1)

    def get_dict(self):
        html = self.get_html_text(self.base_url + '/dict/cate/')
        soup = BeautifulSoup(html, 'lxml')
        for x in soup.findAll('div', {'id': 'dict_nav_list'})[0].findAll('li'):
            self.solve_dict_cate('https://pinyin.sogou.com' + x.a['href'])



if __name__ == '__main__':
    # tmp = 'http://download.pinyin.sogou.com/dict/download_cell.php?id=15142&name=%E4%BA%8C%E4%BA%BA%E8%BD%AC%E8%AF%8D%E6%B1%87%E5%A4%A7%E5%85%A8%E3%80%90%E5%AE%98%E6%96%B9%E6%8E%A8%E8%8D%90%E3%80%91'
    # dl_r = requests.get(tmp)
    # scel_decode = ExtSougouScel()
    # scel_decode.deal_from_content(dl_r.content)
    for line in codecs.open('./fail_tmp', 'r', 'utf-8'):
        if '[fail in]' in line:
            print (line.strip())
            dl_link = re.match('\[fail in\](.*)\[name\]', line).group(1)
            info_dict = {}
            dl_r = requests.get(dl_link)
            scel_decode = ExtSougouScel()
            scel_decode.deal_from_content(dl_r.content)
            exit(-1)

            # f = open('test.data', 'wb')
            # f.write(dl_r.content)
            # exit(-1)
            # info_dict.update(scel_decode.deal_from_content(dl_r.content))

    # set_name = set()
    # for line in codecs.open('./sort_name', 'r', 'utf-8'):
    #     line_list = line.strip().replace('\x00', '').split('\t')
    #     set_name.add(line_list[0])
    # s = SogouSpider()
    # s.load_name(set_name)
    # s.get_dict()

    # print (len(set_name))
    # for line in open('tmp', 'r'):
    # if '[fail in]' in line:
    #     print (line.strip())
