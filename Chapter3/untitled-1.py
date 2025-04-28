import torch
import matplotlib.pyplot as plt

# 生成 10000 个服从标准正态分布的随机数
random_numbers = torch.randn(10000)

# 将张量转换为 NumPy 数组以便绘图
random_numbers_np = random_numbers.numpy()

# 绘制直方图
plt.hist(random_numbers_np, bins=50, density=True)
plt.title('Histogram of torch.randn')
plt.xlabel('Value')
plt.ylabel('Density')
plt.show()
