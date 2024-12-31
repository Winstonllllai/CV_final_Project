# Env state
# info = {
#     "x_pos",  # (int) The player's horizontal position in the level.
#     "y_pos",  # (int) The player's vertical position in the level.
#     "score",  # (int) The current score accumulated by the player.
#     "coins",  # (int) The number of coins the player has collected.
#     "time",   # (int) The remaining time for the level.
#     "flag_get",  # (bool) True if the player has reached the end flag (level completion).
#     "life"   # (int) The number of lives the player has left.
# }


# # simple actions_dim = 7 
# SIMPLE_MOVEMENT = [
#     ["NOOP"],       # Do nothing.
#     ["right"],      # Move right.
#     ["right", "A"], # Move right and jump.
#     ["right", "B"], # Move right and run.
#     ["right", "A", "B"], # Move right, run, and jump.
#     ["A"],          # Jump straight up.
#     ["left"],       # Move left.
# ]
#-----------------------------------------------------------------------------
#獎勵函數
'''
get_coin_reward         : 根據硬幣數量變化提供額外獎勵

'''
'''
環境資訊 (info)
1."x_pos": 水平位置，用於判斷角色的前進情況
2."y_pos": 垂直位置，用於分析跳躍或下落行為
3."score": 玩家目前的遊戲分數
4."coins": 收集到的硬幣數量
5."time": 剩餘時間
5."flag_get": 是否到達終點旗幟（遊戲完成）
6."life": 玩家剩餘的生命數
'''

#===============to do===============================請自定義獎勵函數 至少7個(包含提供的)
#例子:用來獎勵玩家蒐集硬幣的行為
def get_coin_reward(info, reward, prev_info):
    #寫下蒐集到硬幣會對應多少獎勵
    total_reward = reward                                         #獲得目前已有的獎勵數量

    total_reward += (info['coins'] - prev_info['coins']) * 100     #這裡是定義，如果玩家有蒐集到硬幣，則獎勵加10(這裡是可以自己去定義獎勵要給多少的)
    return total_reward
#用來鼓勵玩家進行跳躍或高度變化(因為有時前方有障礙物 會被卡住)
def distance_y_offset_reward(info, reward, prev_info):
    total_reward = reward
    y_offset_change = info['y_pos'] - prev_info['y_pos']
    if y_offset_change > 0:
        total_reward += 5
    elif y_offset_change < 0:
        total_reward += 2
    return total_reward

#用來鼓勵玩家前進，懲罰原地停留或後退
def distance_x_offset_reward(info, reward, prev_info):
    total_reward = reward
    x_offset_change = info['x_pos'] - prev_info['x_pos']
    if x_offset_change > 2:
        total_reward += 5
    elif x_offset_change < -2:
        total_reward += 3
    else:
        total_reward -= 10
    return total_reward

#用來鼓勵玩家完成關卡（到達終點旗幟）
def final_flag_reward(info, reward):
    total_reward = reward
    if info['flag_get']:
        total_reward += 10000
    return total_reward

def score_reward(info, reward, prev_info):
    total_reward = reward
    score = info['score'] - prev_info['score'] - info['score']
    if score > 0:
        total_reward += score
def distance_reward(info, reward, prev_info,distance):
    total_reward = reward
    if info['x_pos'] > distance:
        delta = info['x_pos'] - distance
        distance = info['x_pos']
        total_reward += delta * 5
    return total_reward
def death_penalty(info, reward, prev_info):
    total_reward = reward
    if prev_info['life'] > info['life']:
        total_reward -= 200
    return total_reward

def time_penalty(info, reward, prev_info):
    total_reward = reward
    time_passed = prev_info['time'] - info['time']
    if time_passed > 0:
        total_reward -= time_passed * 0.5
    return total_reward

def stagnation_penalty(reward):
    total_reward = reward
    return total_reward + 100


#===============to do==========================================