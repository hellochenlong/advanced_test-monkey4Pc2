# -*- coding:utf-8 -*-
"""
作者:chenlong
日期：2022/1/28
"""

from PIL import ImageGrab
import time

class Utils:
    def __init__(self):
        pass

    # 每3秒截图一次
    def save_img(self):
        i = 1
        while True:
            img = ImageGrab.grab()
            img.save(f'../data/img{i}.png')
            img.__del__()
            time.sleep(3)
            i += 1
        # img.show()

    def save_img2(self, x1, y1, x2, y2):
        '''

        :param x1: 开始截图的x坐标
        :param y1: 开始截图的y坐标
        :param x2: 结束截图的x坐标
        :param y2: 结束截图的y坐标
        :return:
        '''
        i = 1
        bbox = (x1, y1, x2, y2)
        img = ImageGrab.grab(bbox)
        while True:
            img.save(f'../data/img{i}.png')
            time.sleep(3)
            i += 1
        # img.show()

# if __name__ == '__main__':
#     util = Utils()
#     util.save_img()