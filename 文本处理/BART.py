from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch

# 加载预训练的T5模型和tokenizer
model_name = "utrobinmv/t5_summary_en_ru_zh_base_2048"
model = T5ForConditionalGeneration.from_pretrained(model_name)
tokenizer = T5Tokenizer.from_pretrained(model_name)

# 示例文本（中文）
text = """
    这是一段关于非遗文化的视频字幕，展示了传统手工艺的魅力，讲解了如何制作陶瓷，以及它在当代的传承与创新。
    该视频介绍了中国传统的陶瓷工艺，强调了手工艺的精细和历史意义，并展示了现代社会对这些工艺的保护与发展。
    通过这种方式，视频不仅传承了传统的手工艺，还展示了它在现代社会中的重要性和文化价值。
"""

# 预处理输入文本
inputs = tokenizer(text, return_tensors='pt', max_length=1024, truncation=True)

# 使用T5模型生成摘要
summary_ids = model.generate(
    inputs['input_ids'],
    max_length=150,  # 摘要的最大长度
    num_beams=4,     # beam search的宽度
    early_stopping=True
)

# 解码生成的摘要
summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

# 输出结果
print("Original Text:")
print(text)
print("\nGenerated Summary:")
print(summary)