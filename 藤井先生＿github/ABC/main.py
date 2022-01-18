from ABC import ABC

# パラメーター ----------------------------------------------------------
N = 5   # 次元
function_number = 3   # 課題の関数の番号
num_harvest_bee = 25   # 収穫蜂の数
num_follow_bee = 50
limit_harvest = 200
max_turn = 10   # 最大ターン数
# ---------------------------------------------------------------------

# xの値域は自動化しておく
min_field_list = [-5.0, -5.0, -5.0, -600.0, -10.0, -5.0]
max_field_list = [5.0, 5.0, 10.0, 600.0, 10.0, 5.0]
min_field = min_field_list[function_number - 1]
max_field = max_field_list[function_number - 1]


if __name__ == "__main__" : 
    abc = ABC(N, function_number, num_harvest_bee, num_follow_bee, min_field, max_field, limit_harvest, max_turn)
    #print(abc.harvest_bee_record_list)