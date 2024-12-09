from openai import OpenAI

def call_third_service_video_llm(model_name, content,source='aliyun'):
    if source == 'aliyun':
        call_aliyun_video_llm(model_name, content)
    else:
        print(f'unexpected source type: {source}')


def call_aliyun_video_llm(model_name, content):
    client = OpenAI(
        api_key='xxx',
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    completion = client.chat.completions.create(
        model=model_name,
        messages=[{
            "role": "user",
            "content": content}]
    )
    # 省略答案解析
    return completion.model_dump_json()