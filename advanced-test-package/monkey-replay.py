# -*- coding:utf-8 -*-
"""
作者:chenlong
日期：2022/1/27
"""

import time, random, os
from pymouse import PyMouse
from pykeyboard import PyKeyboard

# 实现Monkey的原样回放，以实现类似于Android ADB Monkey命令中的-s seed.


class MonkeyReplay:
    def __init__(self, waittime):
        self.mouse = PyMouse()
        self.key = PyKeyboard()
        self.waittime = waittime
        self.logname = time.strftime("monkey_%Y%m%d_%H%M%S.txt")
        pass

    # 实现随机移动的功能
    def move(self):
        x = random.randrange(50, 1550)
        y = random.randrange(50, 950)
        self.mouse.move(x, y)
        # print("移动到[%d, %d]位置." % (x, y))
        return x, y

    # 实现单机功能
    def click(self):
        x, y = self.move()
        self.mouse.click(x, y)
        print("在[%d, %d]处，单机." % (x, y))
        self.write_log(f"click;{x};{y}")
        time.sleep(self.waittime)

    # 实现随机输入
    def input(self):
        x, y = self.move()
        input_list = ["test", "123456", "Good Night", "Tomorrow Better!", "Testing", "6666667788", "123.45",
                      "2019-08-08", "13600136001"]
        content = random.choice(input_list)
        self.key.type_string(content)
        print("在[%d, %d]处输入：%s." % (x, y, content))
        self.write_log(f"input;{x};{y};{content}")
        time.sleep(0.5)

    def double_click(self):
        x, y = self.move()
        self.mouse.click(x, y, n=2)
        print("在[%d, %d]处，双机." % (x, y))
        self.write_log(f"double_click;{x};{y}")
        time.sleep(0.5)
        pass

    def right_click(self):
        x, y = self.move()
        self.mouse.click(x, y, button=2)
        print("在[%d, %d]处，右机." % (x, y))
        self.write_log(f"right_click;{x};{y}")
        time.sleep(0.5)
        pass

    def key_press(self):
        x, y = self.move()
        key_list = [self.key.enter_key, self.key.down_key, self.key.space_key, self.key.tab_key, self.key.backspace_key]
        keys_list = [[self.key.control_key, 'c'], [self.key.control_key, 'v'], [self.key.control_key, 'x'],
                     [self.key.alt_key, self.key.function_keys[5]]]
        rate = random.randint(1, 100)
        if rate <= 50:
            # 单个按键
            key = random.choice(key_list)
            self.key.press_key(key)
            print("在[%d, %d]处，按%s键." % (x, y, str(key)))
            self.write_log(f"key_press;{x};{y};{key}")
        else:
            # 组合按键
            keys = random.choice(keys_list)
            self.key.press_keys(keys)
            print("在[%d, %d]处，按%s键." % (x, y, str(keys)))
            self.write_log(f"key_press;{x};{y};{keys}")
        pass

    # 将操作及位置等数据记录到文件中
    def write_log(self, content):
        with open("../data/" + self.logname, "a+") as file:
            file.write(content + '\n')

    # 启动应用程序
    def start_app(self, path):
        os.system('start /b' + path)
        os.popen(path)
        print("启动应用程序成功.")
        time.sleep(self.waittime)

    # 执行随机事件
    def start_test(self, count):
        for i in range(count):
            ratio = random.randint(1, 100)
            if ratio <= 40:
                self.click()
            elif ratio <= 60:
                self.double_click()
            elif ratio <= 80:
                self.key_press()
            else:
                self.input()

    # 读取Monkey日志文件并执行相应事件序列
    def start_replay(self, logname):
        with open("../data/" + logname) as file:
            line_list = file.readlines()

        for line in line_list:
            event = line.strip().split(';')[0]
            x_position = int(line.strip().split(';')[1])
            y_position = int(line.strip().split(';')[2])
            if event == 'input':
                content = line.strip().split(';')[3]
                self.mouse.move(x_position, y_position)
                self.key.type_string(content)
                print("在[%s, %s]处输入%s." % (x_position, y_position, content))
            elif event == 'key_press':
                key_arg = line.strip().split(';')[3]
                self.mouse.move(x_position, y_position)
                list_key_arg = list(key_arg)
                if len(list_key_arg) > 1:
                    self.key.press_keys(list_key_arg)
                    print("在[%s, %s]处，按%s键." % (x_position, y_position, key_arg))
                elif len(list_key_arg) == 1:
                    self.key.press_key(list_key_arg[0])
                    print("在[%s, %s]处，按%s键." % (x_position, y_position, key_arg))
                else:
                    print("参数不合法！！！")
            elif event == 'click':
                self.mouse.click(x_position, y_position)
                print("在[%s, %s]处，单机." % (x_position, y_position))
            elif event == 'double_click':
                self.mouse.click(x_position, y_position, n=2)
                print("在[%s, %s]处，双击." % (x_position, y_position))


if __name__ == '__main__':
    replay = MonkeyReplay(0.5)
    time.sleep(3)
    replay.start_app(r"D:\Mozilla Firefox\firefox.exe")
    # replay.start_test(10)
    replay.start_replay("monkey_20220127_195842.txt")

