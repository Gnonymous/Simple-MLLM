from transformers import Qwen2VLForConditionalGeneration, AutoTokenizer, AutoProcessor
from qwen_vl_utils import process_vision_info

class VlModel:
    def __init__(self, model_dir=None):
        if not model_dir:
            model_dir = 'Qwen2-VL/qwen/Qwen2-VL-2B-Instruct'  # 替换为你的模型权重地址
        self.model = Qwen2VLForConditionalGeneration.from_pretrained(
            model_dir, torch_dtype="auto", device_map="auto"
        )
        self.processor = AutoProcessor.from_pretrained(model_dir)

    def video_chat(self, prompt, image_list):
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "video",
                        "video": image_list,
                        "fps": 1.0,
                    },
                    {"type": "text", "text": prompt},
                ],
            }
        ]
        # Preparation for inference
        text = self.processor.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        image_inputs, video_inputs = process_vision_info(messages)
        inputs = self.processor(
            text=[text],
            images=image_inputs,
            videos=video_inputs,
            padding=True,
            return_tensors="pt",
        )
        inputs = inputs.to("cuda")

        # Inference
        generated_ids = self.model.generate(**inputs, max_new_tokens=128)
        generated_ids_trimmed = [
            out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
        ]
        output_text = self.processor.batch_decode(
            generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
        )
        return output_text