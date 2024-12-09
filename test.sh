# 你好，下午做了个简易的demo，跑通需依赖模型资源，没有做相关的性能测试了
# 1.本地部署的vl模型可以从modelscope下载，我目前机器硬件支持不了本地调试
# 2.可以使用阿里云的百炼接口，需要填api_key，再改一下代码里的调用部分
# demo逻辑流程： 
# 1.一个进程模拟读视频帧，另一个进程模拟接收文本内容（输入省略了asr部分）
# 2.接收到文本内容后，将文本和当前已接收到的视频帧一起作为输入，调用vl模型，获取结果
# 3.当结果打印过程中，如果有新请求中断（用键盘输入模拟VAD识别到新请求的结果），会立即停止当前打印，执行新请求。

image_dir=""

python test_video_thread.py "${image_dir}" &
python test_client.py