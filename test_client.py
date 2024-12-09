import socket
import time

# 与服务端建立连接
def send_request(request):
    client_socket.send(request.encode('utf-8'))
    response = client_socket.recv(1024).decode('utf-8')
    return response

while True:
    try:
        question = input("我在听：")
        #
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("localhost", 8088))
        result = send_request(question)
        print("图文问答响应:", result)
        for char in result:
            time.sleep(0.1)
            print(char, end='', flush=True)
        print()

    except KeyboardInterrupt as e:
        # 需要VAD等技术判断是否有新语音输入
        # 用键盘打断模拟检测到新语音
        print(e)
        print('用户中断，发起新提问')