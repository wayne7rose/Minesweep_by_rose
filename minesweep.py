import pygame as pg
from pygame.locals import *
import random
from math import pi, cos, sin

class MineSweep():
    def __init__(self, x, y , mine_num):
        self.mine = []
        self.neighbor = []
        self.neighbor_flag = 0
        self.x = x
        self.y = y
        self.mine_num = mine_num
        self.list_cue = [0] * self.x * self.y
        self.sweeped = [0] * self.x * self.y
        self.flag = [0] * self.x * self.y

    # 求00-99之间100个数字的横纵坐标
    def get_y(self, n):  # 十位
        return n // self.x
    def get_x(self, n):
        return n % self.x

    def bury_mine(self):
        # 产生随机雷的位置00-99
        list_point = []
        for i in range(self.x * self.y):
            list_point.append(i)    
        random.shuffle(list_point) # 随机排序
        for i in range(self.mine_num):
            self.mine.append(list_point[i])
        # 生成列表list_cue，位置00-99  -->  周围雷的个数cue
        for point in self.mine:
            self.list_cue[point] = 9
            for j in range(8):
                x = int(1.5 * cos(j* pi/4))
                y = int(1.5 * sin(j* pi/4))
                next_point = point + y*self.x + x
                if self.get_x(point) + x in range(self.x) and self.get_y(point) + y in range(self.y):
                    self.list_cue[next_point] += 1
        for i in range(self.x * self.y):
            if self.list_cue[i] > 9:
                self.list_cue[i] = 9
                
        
    # 由一个空白cue=0的point，找到所有邻近的空白cue=0的point
    def find_neighbor(self, point):
        find_all = False
        self.neighbor.append((point, self.list_cue[point]))
        if self.list_cue[point] == 0:
            for j in range(8):
                x = int(1.5 * cos(j* pi/4))
                y = int(1.5 * sin(j* pi/4))
                next_point = point + y*self.x + x
                if self.get_x(point) + x in range(self.x) and self.get_y(point) + y in range(self.y):
                    if (next_point, self.list_cue[next_point]) not in self.neighbor:
                        find_all = True
                        self.find_neighbor(next_point)
        if not find_all:
            return


    # 双击时找到周围所有格子，如果有空白，则打开空白周围所有格子      
    def find_neighbor_8(self, point):
        self.neighbor_flag = 0
        for j in range(8):
            x = int(1.5 * cos(j* pi/4))
            y = int(1.5 * sin(j* pi/4))
            next_point = point + y*self.x + x
            if self.get_x(point) + x in range(self.x) and self.get_y(point) + y in range(self.y):
                if self.flag[next_point] == 0:
                    self.neighbor.append((next_point, self.list_cue[next_point]))
                    if self.list_cue[next_point] == 0:
                        self.find_neighbor(next_point)
                else:
                    self.neighbor_flag += 1


    def neighbor_reset(self):
            self.neighbor = []

            
    def reset(self, x, y, mine_num):
        self.mine = []
        self.x = x
        self.y = y
        self.mine_num = mine_num
        self.neighbor = []
        self.list_cue = [0] * self.x * self.y
        self.sweeped = [0] * self.x * self.y
        self.flag = [0] * self.x * self.y
