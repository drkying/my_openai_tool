# from orderInOkx import order
#
# order({
#     "type": "BTC",
#     "price": 95800,
#     "direction": "空",
#     "win": 94800,
#     "lose": 96500
# })
# import os
#
# from ai2OrderByBot import ai_get_order
from main import judge_obj

# print(ai_get_order('95800附近空比特币，短空的设置96500止损即可，1000点止盈一半，剩余推保本'))
# print(ai_get_order('ETH 2720附近可以埋伏下多单，止损放个2670，看个3400-3500，虽然离现在位置还很遥远，逻辑是重新共振2820大平台，略微刺穿之后获得流动性，重新抽回2820进行支撑确认。这是左侧交易，更安全的做法就是等有一天ETH跌破了2820，重新回到2820之上进行一个横盘调整或回踩，不破位就直接进去，止损放个30点就行。前提是先跌破，后站稳，如果是直接来到2820，并横盘调整就不建议入场'))

# print(isinstance( {'type': 'SOL', 'price': '', 'direction': '空', 'win': '', 'lose': ''}, dict))
# AssistantsId= os.environ.get('OPENAI_ASSISTANTS_ID')
# key = os.environ.get('OPENAI_KEY')
# print(AssistantsId)
# print(key)
print(judge_obj({}))