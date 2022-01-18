from PSO import PSO

# パラメーター ----------------------------------------------------------
N = 5   # 次元
function_number = 2   # 課題の関数の番号
num_agent = 100   # agentの数
max_turn = 1000   # 最大ターン数
# ---------------------------------------------------------------------

# xの値域は自動化しておく
min_field_list = [-5.0, -5.0, -5.0, -600.0, -10.0, -5.0]
max_field_list = [5.0, 5.0, 10.0, 600.0, 10.0, 5.0]
min_field = min_field_list[function_number - 1]
max_field = max_field_list[function_number - 1]


if __name__ == "__main__" : 
    PSO(N, function_number, num_agent, min_field, max_field, max_turn)
