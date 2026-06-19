from torch import nn
import torch
from PIL import Image
from torchvision import transforms
import os

# 原始列表
vegetable_list = ['Bean', 'Bitter_Gourd', 'Bottle_Gourd', 'Brinjal', 'Broccoli', 'Cabbage',
                  'Capsicum', 'Carrot', 'Cauliflower', 'Cucumber', 'Papaya', 'Potato', 'Pumpkin', 'Radish',
                  'Tomato']

# 中文对应列表
chinese_names = ['豌豆', '苦瓜', '蒲瓜', '茄子', '西兰花', '卷心菜', '灯笼椒', '胡萝卜', '花菜', '黄瓜',
                 '木瓜', '土豆', '南瓜', '萝卜', '西红柿']

n_classes = len(chinese_names)


class VegetableCNNModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.network = nn.Sequential(
            nn.Conv2d(in_channels=3, out_channels=100, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(in_channels=100, out_channels=150, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),

            nn.Conv2d(in_channels=150, out_channels=200, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.Conv2d(in_channels=200, out_channels=200, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),

            nn.Conv2d(in_channels=200, out_channels=250, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.Conv2d(in_channels=250, out_channels=250, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),

            nn.Flatten(),
            nn.Linear(250 * 5 * 5, 32),  # 假设输入40x40，经过3次2倍池化后变为5x5
            nn.ReLU(),
            nn.Dropout(0.25),
            nn.Linear(32, n_classes),
        )

    def forward(self, x):
        return self.network(x)


# 创建模型实例
model = VegetableCNNModel()

# 加载模型权重
model_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "model.pth"
    )
)
if os.path.exists(model_path):
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu'), weights_only=True))
model.eval()  # 设置为评估模式


def predict(picture_path):
    image = Image.open(picture_path).convert("RGB")
    transform = transforms.Compose([
        transforms.Resize(40),  # resize最短边到40
        transforms.CenterCrop(40),  # 中心裁剪到40x40
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])
    image_tensor = transform(image).unsqueeze(0)  # 添加batch维度
    with torch.no_grad():
        output = model(image_tensor)
    category_index = output.argmax().item()
    category_name = chinese_names[category_index]
    return category_name