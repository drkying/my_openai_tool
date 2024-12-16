import okx.Account as Account
import okx.Trade as Trade
import okx.PublicData as PublicData

okx_api_key = os.environ.get('OKX_API_KEY')
okx_secret_key = os.environ.get('OKX_SECRET_KEY')
okx_passphrase = os.environ.get('OKX_API_PASSPHRASE')

flag = "0"

accountAPI = Account.AccountAPI(okx_api_key, okx_secret_key, okx_passphrase, False, flag)

import okx.MarketData as MarketData

marketDataAPI = MarketData.MarketAPI(flag = flag)

result = marketDataAPI.get_tickers(instType = "SWAP")
for item in result['data']:
    if item['instId'] == 'BTC-USDT-SWAP':
        print(item)
        break
