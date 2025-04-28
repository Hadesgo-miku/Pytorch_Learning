# clean_file.py
import os

# 1. 指定文件路径
input_path  = 'data/investments_VC.csv'
output_path = 'data/investments_VC_clean.csv'
# 2. 读取原始字节内容
with open(input_path, 'rb') as f:
    raw = f.read()

# 3. 尝试以 utf-8 解码，遇到非法字节就替换为 U+FFFD (即 '�')
text = raw.decode('utf-8', errors='replace')

# 4. 统计非法字符数量
num_illegal = text.count('\ufffd')
print(f"在文件中发现 {num_illegal} 个非法字符（显示为 � ）")

# 5. 替换所有非法字符
clean_text = text.replace('\ufffd', '')

# 6. 保存清理后的文件
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(clean_text)

print(f" 清理完成，已保存到：{output_path}")