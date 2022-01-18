from Agent import Harvest_bee, Follow_bee, Scout_bee
from Function import Function
from Honey import Honey
import time


INF = 1000000000000000000000


class ABC : 
    def __init__(self, N, function_number, num_harvest_bee, num_follow_bee, min_field, max_field, limit_harvest, 
                max_turn, output_interval = 5, output_mode = True) : 
        f = Function(function_number)
        self.N = N
        self.num_harvest_bee = num_harvest_bee
        self.num_follow_bee = num_follow_bee
        self.min_field = min_field 
        self.max_field = max_field
        self.limit_harvest = limit_harvest
        self.max_turn = max_turn
        self.output_mode = output_mode

        self.honey_list = [Honey(f, N, min_field, max_field, limit_harvest) for _ in range(num_harvest_bee)]
        self.harvest_bee_list = [Harvest_bee(f, N, min_field, max_field, limit_harvest, i) for i in range(num_harvest_bee)]
        self.follow_bee_list = [Follow_bee(f, N, min_field, max_field) for _ in range(num_follow_bee)]
        self.scout_bee = Scout_bee(N, min_field, max_field)   # これをlistで持っておく必要はない
        self.gb_score = INF   # とりあえず設定しておく必要がある、負に大きければなんでも良い 
        self.output_interval = output_interval

        # 記録用、可視化にのみ使う
        self.honey_record_list = [[] for _ in range(max_turn)]
        self.harvest_bee_record_list = [[] for _ in range(max_turn)]
        self.follow_bee_record_list = [[] for _ in range(max_turn)]
        self.scout_bee_record_list = [[] for _ in range(max_turn)]
        self.gb_record_list = [[] for _ in range(max_turn)]   # 一つしか入らないが、二次元配列で持っておくと可視化が楽

        # 出力用
        self.parameter_dict = {"harvest" : self.num_harvest_bee, "follow" : self.num_follow_bee, 
                    "limit_harvest" : self.limit_harvest, "max_turn" : self.max_turn}

        self.simulate()

    
    def simulate(self) : 
        print()
        print("------------------------------------- ABC SIMULATION START!!! -------------------------------------")
        print()

        start = int(time.time() * 1000)   # 計算時間の計測、単位は ms

        for turn in range(self.max_turn) : 
            # 記録用、蜜源の位置は更新前に記録しておく
            self.update_honey_record_list(turn)

            # 収穫蜂
            for harvest_bee in self.harvest_bee_list : 
                harvest_bee.step(self.honey_list, self.harvest_bee_record_list, turn)

            # 追従蜂
            for follow_bee in self.follow_bee_list : 
                follow_bee.step(self.honey_list, self.follow_bee_record_list, turn)

            # 偵察蜂
            self.scout_bee.step(self.honey_list, self.scout_bee_record_list, turn)

            # グローバルベストを更新
            self.update_gb(turn)

            # 出力
            if turn % self.output_interval == 0 and self.output_mode == True : 
                self.output(turn)

        end = int(time.time() * 1000)   
        self.calculation_time = end - start

        # 最終結果を出力
        self.final_output()


    # グローバルベストの更新
    def update_gb(self, turn) : 
        for honey in self.honey_list : 
            if honey.score < self.gb_score : 
                self.gb_place = honey.place
                self.gb_score = honey.score
        
        self.gb_record_list[turn].append(self.gb_place)
    

    def update_honey_record_list(self, turn) : 
        for honey in self.honey_list : 
            self.honey_record_list[turn].append(honey.place)


    # 出力
    def output(self, turn) : 
        print("TURN : " + str(turn) + " -------------------------------")
        print("gb_place : " + str(self.gb_place))
        print("gb_score : " + str(self.gb_score))
        print()


    # 最終的な出力
    def final_output(self) : 
        print()
        print("------------------------------- 最終出力 -------------------------------")
        print("パラメータ : ", end = "")
        print(self.parameter_dict)
        print("gb_place : " + str(self.gb_place))
        print("gb_score : " + str(self.gb_score))
        print("計算時間 : " + str(self.calculation_time) + " ms")
        print()


    # 計算時間の出力
    def print_calculation_time(self) : 
        print("計算時間 : " + str(self.calculation_time) + " ms")
        print()


