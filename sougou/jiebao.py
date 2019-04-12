# -*- coding: utf-8 -*-
import struct
import os
import time
import sys

from queue import Queue
from threading import Thread
from pypinyin import lazy_pinyin
import json

PROJECT_PATH = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_PATH)
sys.path.append(os.path.join(PROJECT_PATH, 'sougou'))

import configs
from store_new.stroe import DbToMysql

# 建立一个线程池 用于存入解析完毕的数据
res_queue = Queue()


def byte2ord(data):
    return struct.unpack('H', data)[0]


def byte2chr(data):
    return chr(byte2ord(data))


def byte2str(data):
    return ''.join([byte2chr(data[i:i + 2]) for i in range(0, len(data), 2)])


class ExtSougouScel():
    # 解析搜狗词库文件

    def __init__(self):
        # 拼音表偏移，
        self.startPy = 0x1540
        # 汉语词组表偏移
        self.startChinese = 0x2628
        # 全局拼音表
        self.GPy_Table = {}
        # 元组(词频,拼音,中文词组)的列表
        self.GTable = []

    def getPyTable(self, data):
        # '''获取拼音表'''

        # if data[0:4] != "\x9D\x01\x00\x00":
        #     print 'Are u sure this is a sogou pinyin table?'
        #     return
        data = data[4:]
        pos = 0
        length = len(data)
        while pos < length:
            index = struct.unpack('H', data[pos:pos + 2])[0]
            pos += 2
            l = struct.unpack('H', data[pos:pos + 2])[0]
            pos += 2
            py = byte2str(data[pos:pos + l])
            pos += l
            self.GPy_Table[index] = py

    def getWordPy(self, data):
        # '''获取一个词组的拼音'''
        return ' '.join([self.GPy_Table.get(byte2ord(data[i:i + 2]), '[UNK]') for i in range(0, len(data), 2)])

    def getChinese(self, data):
        # '''读取中文表'''
        pos = 0
        length = len(data)
        while pos < length:
            # 同音词数量
            same = byte2ord(data[pos:pos + 2])
            pos += 2
            # 拼音索引表长度
            py_table_len = byte2ord(data[pos:pos + 2])
            pos += 2
            # 拼音索引表
            py = self.getWordPy(data[pos: pos + py_table_len])
            pos += py_table_len
            # 中文词组
            for i in range(same):
                # 中文词组长度
                c_len = byte2ord(data[pos:pos + 2])
                pos += 2
                # 中文词组
                word = byte2str(data[pos: pos + c_len])
                pos += c_len
                # 扩展数据长度
                ext_len = byte2ord(data[pos:pos + 2])
                pos += 2
                # 词频
                count = byte2ord(data[pos:pos + 2])

                # print (byte2str(data[pos + 2, pos + ext_len]))
                pos += ext_len

                # 保存
                print (c_len, ext_len)
                print (count, py, word)
                # self.GTable.append('\001'.join([count, py, word]))
                # 到下个词的偏移位置

    def deal_from_content(self, data):
        if data[0:12] != b'@\x15\x00\x00DCS\x01\x01\x00\x00\x00':
            print("Are u sure this is sogou scel data")
            exit(-1)
        info_dict = {}
        for i in range(0, len(data), 2):
            if byte2ord(data[i:i+2]) == 0:
                continue
            print ('[', i, i+2, ']', byte2ord(data[i:i+2]), byte2chr(data[i:i+2]))
        exit(-1)
        # print(byte2str(data).replace('\x00', ''))
        # print (byte2str(data).strip().replace('\x00', ''))
        # info_dict['name'] = byte2str(data[0x130:0x338])
        info_dict['type'] = byte2str(data[0x338:0x540]).strip().replace('\x00', '')
        info_dict['describe'] = byte2str(data[0x540:0xd40]).strip().replace('\x00', '')
        # info_dict['raw_example'] =  byte2str(data[0xd40:self.startPy])
        self.getPyTable(data[self.startPy:self.startChinese])
        self.getChinese(data[self.startChinese:])
        info_dict['content'] = ' '.join(self.GTable).strip().replace('\x00', '')
        exit(-1)
        return info_dict
        # print (self.GPy_Table)
        # exit(-1)
