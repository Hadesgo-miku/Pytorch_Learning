
import sys
import torch
print(torch.__version__)
print(sys.executable)
print(sys.version)# 应该显示你的conda环境路径

torch.device('mps')