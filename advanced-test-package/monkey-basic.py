# -*- coding:utf-8 -*-
"""
作者:chenlong
日期：2022/1/18
"""


import os, time, random
from pymouse import PyMouse
from pykeyboard import PyKeyboard
import uiautomation
from utils import monkey_utils
import threading

# os.system('adb shell monkey -p com.grsisfee.zqfaeandroid 2000')

'''
#一个monkey测试工具，解决哪些问题
#1.如何模拟随机操作的问题？通过PyUserInput(PyMouse和Pykeyboard)+光标的随机移动（生成随机坐标）。
#2.通过生成随机数的方式来指定每一次执行一个事件时，事件本身是随机的。
#3.输入的内容还没有实现随机(电话号码:130000000000-19999999999)
#4.没有模拟键盘快捷方式或快捷键操作，比如回车，组合按键(ctrl+C/V)等
#5.如何确保被测应用一定是指定的应用而不是整个操作系统级
#6.如果应用程序不是最大化（即使是最大化，也有可能点击到任务栏），如何确保鼠标的随机移动必然在该应用程序窗口内。
#7.如果不小心把窗口点到后面去了（失去焦点），如何处理这样的异常？

'''


class MonkeyTest:
    def __init__(self):
        self.mouse = PyMouse()
        self.key = PyKeyboard()
        self.rectangle = None
        pass

    def move(self):
        x = random.randrange(self.rectangle.left + 20, self.rectangle.right - 20)
        y = random.randrange(self.rectangle.top + 20, self.rectangle.bottom - 20)
        self.mouse.move(x, y)
        time.sleep(0.5)
        return x, y
        pass

    def click(self):
        x, y = self.move()
        self.mouse.click(x, y)
        time.sleep(0.5)
        pass

    def double_click(self):
        x, y = self.move()
        self.mouse.click(x, y, n=2)
        time.sleep(0.5)
        pass

    def right_click(self):
        x, y = self.move()
        self.mouse.click(x, y, button=2)
        time.sleep(0.5)
        pass

    def input(self):
        input_list = ["test", "123456", "Good Night", "Tomorrow Better!", "Testing", "6666667788", "123.45",
                      "2019-08-08", "13600136001"]
        content = random.choice(input_list)
        self.key.type_string(content)
        time.sleep(0.5)
        pass

    def key_press(self):
        key_list = [self.key.enter_key, self.key.down_key, self.key.space_key, self.key.tab_key, self.key.backspace_key]
        keys_list = [[self.key.control_key, 'c'], [self.key.control_key, 'v'], [self.key.control_key, 'x'],
                     [self.key.alt_key, self.key.function_keys[5]]]
        rate = random.randint(1, 100)
        if rate <= 50:
            # 单个按键
            key = random.choice(key_list)
            self.key.press_key(key)
        else:
            # 组合按键
            keys = random.choice(keys_list)
            self.key.press_keys(keys)
        pass


if __name__ == '__main__':
    monkey = MonkeyTest()
    time.sleep(2)

    window = uiautomation.WindowControl(Name='公司相关制度.pdf - 迅读PDF大师')
    window.SetTopmost(True) #保持窗口始终位于顶部，保证不会失去焦点
    # print(window.BoundingRectangle)
    monkey.rectangle = window.BoundingRectangle

    utils = monkey_utils.Utils()

    # 开启守护线程
    th1 = threading.Thread(target=utils.save_img)
    th1.setDaemon(True)
    th1.start()

    for i in range(20):
        ratio = random.randint(1, 100)
        if ratio <= 40:
            monkey.click()
        elif ratio <= 60:
            monkey.double_click()
        elif ratio <= 80:
            monkey.key_press()
        else:
            monkey.input()
