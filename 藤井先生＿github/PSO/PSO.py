from Agent import Agent
from Function import Function
import time

INF = 1000000000000000000000000000000

class PSO : 
    def __init__(self, N, function_number, num_agent, min_field, max_field, max_turn, w, c1, c2, 
                output_interval = 5, output_mode = True) : 
        f = Function(function_number)
        self.num_agent = num_agent
        self.max_turn = max_turn
        self.w = w
        self.c1 = c1 
        self.c2 = c2
        self.output_interval = output_interval
        self.output_mode = output_mode

        self.parameter_dict = {"num_agent" : num_agent, "max_turn" : max_turn, "w" : w, "c1" : c1, "c2" : c2}

        self.agent_list = [Agent(f, N, min_field, max_field, w, c1, c2) for _ in range(num_agent)]   # 全てのagentを持っておく配列
        self.gb_score = INF   # とりあえず適当な数に設定しておく、大きければなんでも良い

        # 記録、可視化のみに使う
        self.agent_place_list = [[] for _ in range(max_turn)]
        self.gb_record_list = [[] for _ in range(max_turn)]   # 一つしか入らないが、二次元配列で持っておくと可視化が楽

        self.update_gb(0, False)   # 初期状態でのgb_place及びgb_scoreを記録しておく

        self.simulate()   # PSOシミュレーション


    # PSOシミュレーション
    def simulate(self) : 
        print()
        print("------------------------------ PSO SIMULATION START!! ------------------------------")
        print()

        start = int(time.time() * 1000)   # 計算時間の計測、単位は ms

        for turn in range(self.max_turn) : 
            for agent in self.agent_list : 
                agent.step(self.gb_place, self.agent_place_list, turn)   # 各agentの状態を更新
            self.update_gb(turn, True)

            if turn % self.output_interval == 0 and self.output_mode == True :   # output_intervalおきに出力
                self.output(turn)

        end = int(time.time() * 1000)   # 計算時間の計測、単位は ms
        self.calculation_time = end - start
        
        self.final_output()   # これが最終結果


    # グローバルベストの更新
    def update_gb(self, turn, update_flag) : 
        for agent in self.agent_list : 
            if agent.pb_score < self.gb_score : 
                self.gb_score = agent.pb_score
                self.gb_place = agent.pb_place

        if update_flag == False :   # 最初のターンはself.gb_record_listを更新しない
            pass
        else : 
            self.gb_record_list[turn].append(self.gb_place)


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

