from transformers import BertTokenizer, BertModel
import torch

# 加载中文BERT模型
tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
model = BertModel.from_pretrained('bert-base-chinese')
print('加载完成')
# 示例视频字幕
subtitle = "这是一段关于非遗文化的视频字幕，展示了传统手工艺的魅力。"

# 编码文本
inputs = tokenizer(subtitle, return_tensors="pt", truncation=True, padding=True)
print('编码完成')
# 获取BERT模型的输出
outputs = model(**inputs)

# 提取[CLS] Token的隐藏状态（最后一层）
cls_embedding = outputs.last_hidden_state[:, 0, :]  # CLS位置的嵌入向量
print('提取完成')
print(cls_embedding)