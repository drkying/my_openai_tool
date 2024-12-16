import json
import os
import time

from openai import OpenAI

from log_e2btc import log_e2btc

AssistantsId= os.environ.get('OPENAI_ASSISTANTS_ID')
key = os.environ.get('OPENAI_KEY')

client = OpenAI(
    api_key=key
)

thread = client.beta.threads.create()


def ai_get_order(message):
    log_e2btc('接收的消息', message)
    # 每次开始前，删除之前的消息
    templist = client.beta.threads.messages.list(
        thread_id=thread.id
    )
    for temp in reversed(templist.data):
        client.beta.threads.messages.delete(thread_id=thread.id, message_id=temp.id)

    # 通过openai的Assistants模型来获取结果，而不需要自己构造prompt
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=message
    )
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=AssistantsId
    )

    # Waits for the run to be completed.
    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if run_status.status == "completed":
            break
        elif run_status.status == "failed":
            log_e2btc("请求bot失败:", run_status.last_error)
            break
        time.sleep(2)  # wait for 2 seconds before checking again

    # Step 5: Parse the Assistant's Response to Print the Results
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )

    for message in reversed(messages.data):
        role = message.role
        for content in message.content:
            if content.type == 'text' and role == 'assistant':
                response = content.text.value
                parsed_content = json.loads(response.strip('```json\n').strip('\n```'))
                log_e2btc('解析后的内容，即生成的订单：', parsed_content)
                return parsed_content
