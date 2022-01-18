import numpy as np 
import random 
import math
from Honey import Honey


INF = 1000000000000000000000000000
epsilon = 0.00000000000000001


class Harvest_bee : 
    def __init__(self, f, N, min_field, max_field, limit_harvest, honey_number) : 
        self.f = f
        self.N = N
        self.min_field = min_field
        self.max_field = max_field
        self.limit_harvest = limit_harvest   # 何回まで同じ蜜源を探索するか
        self.honey_number = honey_number


    # 1ターンでのagentの行動
    def step(self, honey_list, harvest_bee_record_list, turn) : 
        honey = honey_list[self.honey_number]   # この蜂が持つ蜜源

        another_honey_number = "_"   # 蜜源の更新に使う別の蜜源、初期値は適当
        while True : 
            another_honey_number = random.randint(0, len(honey_list) - 1)
            if another_honey_number == self.honey_number :   # anotherが自身と同じになったらやり直し
                continue
            else : 
                break
        another_honey = honey_list[another_honey_number]

        r = np.array([random.uniform(-1, 1) for _ in range(self.N)])
        self.place = update_place(honey, another_honey, r)   # self.placeを計算する
        self.score = self.f(self.place)

        # 記録用、可視化以外では使わない
        harvest_bee_record_list[turn].append(self.place)

        # self.placeのスコアが元のスコアより良かったら更新する。参照渡しに注意（Pythonの沼）
        if self.score < honey.score : 
            honey_list[self.honey_number].count = 0
            honey_list[self.honey_number].place = self.place
            honey_list[self.honey_number].score = self.score
        else : 
            honey_list[self.honey_number].count += 1 


class Follow_bee : 
    def __init__(self, f, N, min_field, max_field) : 
        self.f = f
        self.N = N
        self.min_field = min_field
        self.max_field = max_field
        self.pos_place = np.array([0 for _ in range(N)])


    def step(self, honey_list, follow_bee_record_list, turn) : 
        chosen_honey_number = self.choose_honey(honey_list)   # 更新の対象となる蜜源の番号
        chosen_honey = honey_list[chosen_honey_number]   # 更新の対象となる蜜源

        another_honey_number = "_"   # 蜜源の更新に使う別の蜜源、初期値は適当
        while True : 
            another_honey_number = random.randint(0, len(honey_list) - 1)
            if another_honey_number == chosen_honey_number :   # anotherが今見ている蜜源と同じになったらやり直し
                continue
            else : 
                break
        another_honey = honey_list[another_honey_number]

        r = np.array([random.uniform(-1, 1) for _ in range(self.N)])
        self.place = update_place(chosen_honey, another_honey, r)   # 追従蜂の場所の更新
        self.score = self.f(self.place)

        # 記録用、可視化にしか使わない
        follow_bee_record_list[turn].append(self.place)

        # 更新
        if self.score < chosen_honey.score : 
            honey_list[chosen_honey_number].count = 0
            honey_list[chosen_honey_number].place = self.place
            honey_list[chosen_honey_number].score = self.score
        else : 
            honey_list[chosen_honey_number].count += 1
    

    # 追従蜂がどの蜜源を選ぶか。番号で返すことにする
    def choose_honey(self, honey_list) : 
        max_score = -1 * INF   # これを使って各スコアを修正する
        for honey in honey_list : 
            if max_score < honey.score : 
                max_score = honey.score

        total_score_list = []   # 0からi番目までのスコアの和を入れておく
        for i, honey in enumerate(honey_list) : 
            if i == 0 : 
                total_score_list.append(max_score - honey.score)   # max_scoreで補正
            else : 
                total_score_list.append((max_score - honey.score) + total_score_list[-1])   # min_scoreで補正

        # total_score_list=[0,1,2,3,4,5]でr=3.5なら4を選ぶ
        chosen_honey_number = "_"   # とりあえず宣言しておく
        r = random.uniform(0, total_score_list[-1])
        for i in range(len(honey_list)) : 
            if total_score_list[i] >= r : 
                chosen_honey_number = i
                break
        
        return chosen_honey_number


class Scout_bee : 
    def __init__(self, N, min_field, max_field) :
        self.N = N 
        self.min_field = min_field
        self.max_field = max_field  


    def step(self, honey_list, scout_bee_record_list, turn) : 
        for i in range(len(honey_list)) : 
            # 最大回数収穫した、等号はどちらでも良いと思う（授業スライド的には">"だが、直感的にはこちらがわかりやすいので、こちらにしておく）
            if honey_list[i].count >= honey_list[i].limit_harvest : 
                honey_list[i].place = np.array([random.uniform(self.min_field, self.max_field) for _ in range(self.N)])   # 適当な場所に
                honey_list[i].count = 0

                # 記録用、可視化以外では使わない
                scout_bee_record_list[turn].append(honey_list[i].place)
            else : 
                pass
        

# 場所を更新する。この時、値域外にでてしまう可能性があるので、注意する
# 値域外にでてしまう時は、値域の「壁」で止まるという処理にする
def update_place(honey, another_honey, r) : 
    vector = r * (honey.place - another_honey.place)   # この向きに進む
    min_c = INF   # vectorにmin_cを掛けると、ある次元で壁にぶつかる。これが1以下の時は壁にぶつかってしまう

    for i in range(honey.place.size) : 
        if abs(vector[i]) < epsilon :   # 探索が収束してくると、たまにvector[i]が0になってしまうので、vector[i]が微小ならスキップする
            continue
        elif vector[i] > 0 : 
            distance = honey.max_field - honey.place[i]   # ある次元での壁との距離
            c = math.floor(distance * 1000 / vector[i]) / 1000   # 床関数を使うことによって、壁を超えない様にする
            min_c = min(min_c, c)
        else : 
            distance = honey.min_field - honey.place[i]   # vector[i]が負なので、distanceも負にしておかなければならない
            c = math.floor(distance * 1000 / vector[i]) / 1000   # 床関数を使うことによって、壁を超えない様にする
            min_c = min(min_c, c)
    
    if min_c >= 1 :   # 壁を超えない時の処理
        return honey.place + vector
    else :   # 壁を超える時の処理。vectorにmin_cを掛けて、壁で止まる様にする
        return honey.place + vector * min_c