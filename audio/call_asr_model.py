
from http import HTTPStatus
import dashscope
import json

def call_third_service_asr(model_name, wavs,source='aliyun'):
    if source == 'aliyun':
        call_aliyun_asr(model_name, wavs)
    else:
        print(f'unexpected source type: {source}')


def call_aliyun_asr(model_name, wavs):
    dashscope.api_key = 'xxx'

    task_response = dashscope.audio.asr.Transcription.async_call(
        model=model_name,
        file_urls=wavs,
        language_hints=['zh', 'en']
    )

    transcribe_response = dashscope.audio.asr.Transcription.wait(task=task_response.output.task_id)
    if transcribe_response.status_code == HTTPStatus.OK:
        # 省略解析过程
        return json.dumps(transcribe_response.output, indent=4, ensure_ascii=False)
    else:
        raise