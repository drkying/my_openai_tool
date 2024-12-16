#将传入的内容转化成str,可能会有多个参数,写入tg.txt文件并换行作为日志记录
## 记得解决中文输入文件后乱码的问题
def log_e2btc(*content):
    try:
        with open('tg.txt', 'a', encoding='utf-8') as f:
            f.write(str(content) + '\n')
    except Exception as e:
        print('写入文件失败', e)