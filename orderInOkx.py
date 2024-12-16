import os

import okx.Account as Account
import okx.Trade as Trade
import okx.MarketData as MarketData
import okx.PublicData as PublicData
from log_e2btc import log_e2btc
# okx_api_key = 'b65c4d9d-a16d-44e7-8ad9-2263d94e0955'
# okx_secret_key = '25632A9D5E49EF1E114ECFE3873E8598'
# okx_passphrase = '@qQ112233'

okx_api_key = os.environ.get('OKX_API_KEY')
okx_secret_key = os.environ.get('OKX_SECRET_KEY')
okx_passphrase = os.environ.get('OKX_API_PASSPHRASE')


flag = "0"  # 实盘: 0, 模拟盘: 1

accountAPI = Account.AccountAPI(okx_api_key, okx_secret_key, okx_passphrase, False, flag)

tradeAPI = Trade.TradeAPI(okx_api_key, okx_secret_key, okx_passphrase, False, flag)

marketDataAPI = MarketData.MarketAPI(flag = flag)
publicDataAPI = PublicData.PublicAPI(flag = flag)

result = accountAPI.get_account_config()
log_e2btc("okx_result:登录成功",result)
def order(res):
    # Determine the amount to buy based on the type of currency
    if res['type'] in ['BTC', 'ETH']:
        usdt_amount = 1000
        leverage = 100
    elif res['type'] in ['BNB', 'SOL']:
        usdt_amount = 500
        leverage = 50
    else:
        usdt_amount = 100
        leverage = 10


    current_price = ''

    for item in marketDataAPI.get_tickers(instType = "SWAP")['data']:
        if item['instId'] == res['type'] + '-USDT-SWAP':
            log_e2btc(item)
            current_price = item['last']
            break

    if not current_price:
        #未获取到价格，不下单
        return
    amount = usdt_amount / float(current_price)


    publicdata = {}
    for item in publicDataAPI.get_instruments(instType = "SWAP")['data']:
        if item['instId'] == res['type'] + '-USDT-SWAP':
            log_e2btc(item)
            publicdata = item
            break


    if not publicdata:
        #未获取到合约信息，不下单
        return
    size = amount / (float(publicdata['ctVal']) * float(publicdata['ctMult']))
    #size 取整数，小于一时不下单
    if size < 1:
        return
    size = int(size)
    log_e2btc('size',size)


    log_e2btc(res['type'] + '设置杠杆')
    log_e2btc(accountAPI.set_leverage(
        instId=res['type'] + "-USDT-SWAP",
        lever=str(leverage),
        mgnMode="cross"
    ))

    # Place an order
    order_info = {
        'instId': res['type'] + '-USDT-SWAP',
        'tdMode': 'cross',
        'side': 'buy' if res['direction'] == '多' else 'sell',
        'posSide': 'long' if res['direction'] == '多' else 'short',
        'ordType': 'limit',
        'px': res['price'],
        'sz': size,
        'attachAlgoOrds': [
            {
                'tpOrdKind': 'condition',
                'tpTriggerPx': res['win'],
                'tpOrdPx': '-1',
                'slTriggerPx': res['lose'],
                'slOrdPx': '-1',
                'tpTriggerPxType': 'last',
                'slTriggerPxType': 'mark',
            }
        ],
    }
    response = tradeAPI.place_order(**order_info)
    log_e2btc('下单结果')
    log_e2btc(response)