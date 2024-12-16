# import openai
import json
import os

from log_e2btc import log_e2btc
key = os.environ.get('OPENAI_KEY')

from openai import OpenAI

client = OpenAI(
    api_key=key
)


def ai_get_order(message):
    prompt = f"我将提供一段话，这段话可能包含虚拟货币投资建议，请你分析他并返回以下格式的结果：{{ 'type':'提到的货币类型，如BTC、SOL、ETH等' ， 'price' :'推荐的价格，如果是一个区间则取中间值' , 'direction' :'方向，多还是空' ,'win' : '止盈价格' , 'lose' :'止损价格' }}， 如果不包含，则返回{{}}。请注意，仅输出json，不需要其他内容，以下是提供的话：\n\n{message}"
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-4o",
    )
    # log_e2btc(response)
    content = response.choices[0].message.content

    log_e2btc('原始内容：', content)

    # Parse the content field as JSON
    parsed_content = json.loads(content.strip('```json\n').strip('\n```'))

    log_e2btc('解析后的内容：', parsed_content)

    return parsed_content
