import os
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms
import torch.optim as optim
from tqdm import tqdm
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dlmodel import VegetableCNNModel, n_classes


def download_dataset():
    try:
        import opendatasets as od
        dataset_url = "https://www.kaggle.com/misrakahmed/vegetable-image-dataset"
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

        if not os.path.exists(data_dir):
            print("Downloading dataset...")
            od.download(dataset_url, os.path.dirname(data_dir))
            print("Dataset downloaded successfully!")

        actual_data_path = os.path.join(data_dir, 'vegetable-image-dataset', 'Vegetable Images')
        if os.path.exists(actual_data_path):
            import shutil
            for item in os.listdir(actual_data_path):
                src = os.path.join(actual_data_path, item)
                dst = os.path.join(data_dir, item)
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.move(src, data_dir)
            shutil.rmtree(os.path.join(data_dir, 'vegetable-image-dataset'))

        return data_dir
    except Exception as e:
        print(f"Error downloading dataset: {e}")
        print("Please download manually from: https://www.kaggle.com/misrakahmed/vegetable-image-dataset")
        return None


def train_model():
    data_dir = download_dataset()

    if data_dir is None or not os.path.exists(data_dir):
        print("Error: Dataset not found")
        return

    transform = transforms.Compose([
        transforms.Resize(40),
        transforms.CenterCrop(40),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    full_dataset = datasets.ImageFolder(root=data_dir, transform=transform)

    train_size = int(0.7 * len(full_dataset))
    val_size = int(0.15 * len(full_dataset))
    test_size = len(full_dataset) - train_size - val_size

    train_dataset, val_dataset, test_dataset = random_split(full_dataset, [train_size, val_size, test_size])

    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=4)
    val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False, num_workers=4)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False, num_workers=4)

    model = VegetableCNNModel()

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)
    print(f"Using {device} for training")

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    num_epochs = 50
    best_val_acc = 0.0

    for epoch in range(num_epochs):
        model.train()
        train_loss = 0.0
        train_correct = 0

        for images, labels in tqdm(train_loader, desc=f'Epoch {epoch + 1}/{num_epochs}'):
            images = images.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            train_loss += loss.item() * images.size(0)
            _, preds = torch.max(outputs, 1)
            train_correct += torch.sum(preds == labels.data)

        train_loss = train_loss / len(train_dataset)
        train_acc = train_correct.double() / len(train_dataset)

        model.eval()
        val_loss = 0.0
        val_correct = 0

        with torch.no_grad():
            for images, labels in val_loader:
                images = images.to(device)
                labels = labels.to(device)

                outputs = model(images)
                loss = criterion(outputs, labels)

                val_loss += loss.item() * images.size(0)
                _, preds = torch.max(outputs, 1)
                val_correct += torch.sum(preds == labels.data)

        val_loss = val_loss / len(val_dataset)
        val_acc = val_correct.double() / len(val_dataset)

        print(f'Epoch {epoch + 1}/{num_epochs}')
        print(f'Train Loss: {train_loss:.4f} Acc: {train_acc:.4f}')
        print(f'Val Loss: {val_loss:.4f} Acc: {val_acc:.4f}')
        print('-' * 50)

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dlmodel', 'model.pth')
            torch.save(model.state_dict(), model_path)
            print(f'Saved best model with val_acc: {best_val_acc:.4f}')

    model.load_state_dict(torch.load(model_path))
    model.eval()
    test_correct = 0

    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)
            _, preds = torch.max(outputs, 1)
            test_correct += torch.sum(preds == labels.data)

    test_acc = test_correct.double() / len(test_dataset)
    print(f'Final Test Accuracy: {test_acc:.4f}')


if __name__ == '__main__':
    train_model()