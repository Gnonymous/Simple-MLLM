import socket
import time
import os
import sys

def send_video_request(_v_client_socket, _video_dir='default_dir'):
    try:
        fn_list = os.listdir(_video_dir)

        for fn in fn_list:
            # 模拟每秒10帧
            image_url = os.path.join(_video_dir, fn)
            _v_client_socket.send(image_url.encode('utf-8'))
            time.sleep(0.1)
    except Exception as e:
        print('read image file failed. error: \n')
        print(e)


if __name__ == '__main__':
    # 异步模拟视频输入
    v_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    v_client_socket.connect(("localhost", 8099))

    # send_video_request(v_client_socket)
    video_dir = sys.argv[1]
    send_video_request(v_client_socket, video_dir)
