import random
import math
import numpy as np


INF = 100000000000000000000
epsilon = 0.00000000000000001


class Agent : 
    def __init__(self, f, N, min_field, max_field, w, c1, c2) : 
        self.f = f   # 対象の関数
        self.N = N   #　次元
        self.min_field = min_field   # xの最小値
        self.max_field = max_field   # xの最大値
        self.w = w   # 速度ベクトルのパラメータ、下の二つも同じ
        self.c1 = c1
        self.c2 = c2

        # 初期設定
        self.v = np.array([random.random() - 0.5 for _ in range(N)])   # 初期速度
        self.pos_place = np.array([random.uniform(min_field, max_field) for _ in range(N)])   # 初期位置
        self.pb_place = self.pos_place   # 自己ベストを出した時の場所（pb = personal_best）
        self.pb_score = f(self.pos_place)   # 自己ベストのスコア


    # 速度、位置、パーソナルベストの更新
    def step(self, gb_place, agent_place_list, turn) :   
        r1 = random.random()
        r2 = random.random()

        # 速度と位置の更新
        self.v = self.w * self.v + self.c1 * r1 * (self.pb_place - self.pos_place) + self.c2 * r2 * (gb_place - self.pos_place)
        self.update_place()   # pos_placeの更新
        agent_place_list[turn].append(self.pos_place)

        # パーソナルベストの更新
        if self.f(self.pos_place) < self.pb_score : 
            self.pb_score = self.f(self.pos_place)
            self.pb_place = self.pos_place


    # 場所を更新する。この時、値域外にでてしまう可能性があるので、注意する
    # 値域外にでてしまう時は、指定された向きに進んでいって、値域の「壁」で止まるという処理にする
    def update_place(self) : 
        min_c = INF   # self.vにmin_cを掛けてself.pos_placeに足すと、ある次元で壁にぶつかる。これが1以下の時は壁にぶつかってしまう

        for i in range(self.v.size) : 
            if abs(self.v[i] < epsilon) :   # 探索が収束してくると、たまにv[i]が0になってしまうので、v[i]が微小ならスキップする
                continue
            elif self.v[i] > 0 : 
                distance = self.max_field - self.pos_place[i]   # ある次元での壁との距離
                c = math.floor(distance * 1000 / self.v[i]) / 1000   # 床関数を使うことによって、壁を超えない様にする
                min_c = min(min_c, c)
            else : 
                distance = self.min_field - self.pos_place[i]   # self.vが負なので、distanceも負にしておかなければならない
                c = math.floor(distance * 1000 / self.v[i]) / 1000   # 床関数を使うことによって、壁を超えない様にする
                min_c = min(min_c, c)
    
        if min_c >= 1 :   # 壁を超えない時の処理
            self.pos_place = self.pos_place + self.v
        else :   # 壁を超える時の処理。self.vにmin_cを掛けて、壁で止まる様にする
            self.pos_place = self.pos_place + min_c * self.v

        
        