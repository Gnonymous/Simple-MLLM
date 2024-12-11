import socketserver
import threading
import sys

sys.path.append('./')
sys.path.append('../')
import video.call_vl_model
import audio.call_asr_model
from video.vl_model import VlModel

# 这里只是占位，实际中需要替换为真正处理视频信息的相关逻辑和模型调用等
VIDEO_INFO = []  # 模拟存储视频信息数据

# 处理视频信息相关服务的类（模拟常驻且能获取视频信息数据，实际功能需完善）
class VideoInfoHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            try:
                data = self.request.recv(1024).decode('utf-8')
                if not data:
                    break
                # 保存图片列表
                VIDEO_INFO.append(data)
            except ConnectionResetError:
                break


# 处理图文问答相关服务的类（实际需对接对应模型或接口等）
class ImageTextQAHandler(socketserver.BaseRequestHandler):
    def handle(self):
        v_model = VlModel
        while True:
            try:
                # 省略语音内容转asr步骤，假设得到文本开始处理
                data = self.request.recv(1024).decode('utf-8')
                # TODO 处理VAD结果，通过ASR转文本
                # TODO 按业务需要加更复杂的语音分类和情感分析等
                # TODO 处理历史信息，生成当前轮的prompt

                # 如果使用三方asr信息，需要上传语音文件到公开路径
                # wav_url = "http://xxx"
                # data = call_third_service_asr(model_name='paraformer', wav=wav_url, source='aliyun')
                if not data:
                    break
                # 处理当前图片帧集合，配合输入的语音转文本的内容，一并输入vl模型
                # 如调用接口实现，需要能访问到视频列表里的每个图片帧地址，伪代码大致如下：
                # response = call_third_service_video_llm(model_name='qwen-vl-max', content=content, source='aliyun')
                # content = [
                #     {
                #         "type": "video",
                #         "video": VIDEO_INFO  # list: ["http://xxx-000.jpg", "http://xxx-001.jpg", ...]
                #         "fps": 10.0,
                #     },
                #     {"type": "text", "text": data},
                # ]
                # response = '这是模拟图文问答的回复'

                # 本地调用demo。modelscope
                response = v_model.video_chat(data, VIDEO_INFO)
                info_log = f"用户输入:{data},当前视频长度:{len(VIDEO_INFO)},模型回复:{response}"
                print(info_log)
                 # 修改部分：检查 response 类型并转化为字符串
                if isinstance(response, list):
                    response = "\n".join(response)  # 或者使用 str(response)
                self.request.send(response.encode('utf-8'))
            except ConnectionResetError:
                break


if __name__ == "__main__":
    HOST = "localhost"
    server = socketserver.ThreadingTCPServer((HOST, 8099), VideoInfoHandler)
    video_thread = threading.Thread(target=server.serve_forever)
    video_thread.start()  # 启动处理视频信息的服务并常驻

    # 创建另一个用于处理图文问答的服务，使用相同的主机和端口（可根据实际调整）
    qa_server = socketserver.ThreadingTCPServer((HOST, 8088), ImageTextQAHandler)
    qa_thread = threading.Thread(target=qa_server.serve_forever)
    qa_thread.start()  # 启动图文问答服务