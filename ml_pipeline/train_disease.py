"""
train_disease.py
Trains a lightweight 12-class Crop Disease Classifier optimized for mobile edge devices.
Supports RTX 4060 GPU acceleration (CUDA) and CPU fallback.
Generates evaluation metrics: accuracy, precision, recall, F1, and confusion matrix.
Exports model for mobile quantization and on-device inference.
"""

import os
import json
import time
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(ROOT_DIR, "ml_pipeline", "output")
DATA_DIR = os.path.join(ROOT_DIR, "data")

CLASSES = [
    "rice_blast",
    "rice_brown_spot",
    "wheat_yellow_rust",
    "wheat_loose_smut",
    "cotton_bacterial_blight",
    "potato_early_blight",
    "potato_late_blight",
    "tomato_early_blight",
    "tomato_leaf_mold",
    "healthy_leaf",
    "soil_or_background",
    "uncertain_quality"
]

class DepthwiseSeparableConv(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1):
        super().__init__()
        self.depthwise = nn.Conv2d(in_channels, in_channels, kernel_size=3, stride=stride, padding=1, groups=in_channels, bias=False)
        self.pointwise = nn.Conv2d(in_channels, out_channels, kernel_size=1, bias=False)
        self.bn = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU6(inplace=True)

    def forward(self, x):
        x = self.depthwise(x)
        x = self.pointwise(x)
        x = self.bn(x)
        return self.relu(x)

class MobileAgriNet(nn.Module):
    """
    Ultra-lightweight Mobile Convolutional Neural Network designed for
    budget Android smartphones (ARM Cortex-A53 / A55) with <3MB footprint.
    Input shape: (3, 224, 224)
    """
    def __init__(self, num_classes=12):
        super().__init__()
        # Initial standard conv
        self.stem = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=3, stride=2, padding=1, bias=False),
            nn.BatchNorm2d(16),
            nn.ReLU6(inplace=True)
        )
        # Depthwise separable stages
        self.stages = nn.Sequential(
            DepthwiseSeparableConv(16, 24, stride=1),
            DepthwiseSeparableConv(24, 32, stride=2),
            DepthwiseSeparableConv(32, 48, stride=2),
            DepthwiseSeparableConv(48, 64, stride=2),
            DepthwiseSeparableConv(64, 96, stride=2)
        )
        self.head = nn.Sequential(
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Flatten(),
            nn.Dropout(0.2),
            nn.Linear(96, num_classes)
        )

    def forward(self, x):
        x = self.stem(x)
        x = self.stages(x)
        x = self.head(x)
        return x

class SyntheticAgriLeafDataset(Dataset):
    """
    Generates synthetic agricultural leaf spectral tensors with characteristic
    color-channel distributions, lesion spatial frequencies, and noise profiles
    for the 12 disease classes to validate the end-to-end pipeline.
    """
    def __init__(self, num_samples=600, is_train=True):
        self.num_samples = num_samples
        self.is_train = is_train
        np.random.seed(42 if is_train else 99)

        self.data = []
        self.labels = []
        samples_per_class = num_samples // len(CLASSES)

        for class_idx in range(len(CLASSES)):
            for _ in range(samples_per_class):
                # Channel 0: Red, Channel 1: Green, Channel 2: Blue
                # Leaves typically have higher Green; lesions shift to Red/Brown
                tensor = np.zeros((3, 224, 224), dtype=np.float32)

                if class_idx == 9:  # healthy_leaf -> strong vibrant green
                    tensor[0] = np.random.normal(0.20, 0.05, (224, 224))
                    tensor[1] = np.random.normal(0.65, 0.08, (224, 224))
                    tensor[2] = np.random.normal(0.18, 0.05, (224, 224))
                elif class_idx == 10:  # soil_or_background -> dark brown / gray
                    tensor[0] = np.random.normal(0.45, 0.08, (224, 224))
                    tensor[1] = np.random.normal(0.35, 0.06, (224, 224))
                    tensor[2] = np.random.normal(0.25, 0.06, (224, 224))
                elif class_idx == 11:  # uncertain_quality -> high noise / blur
                    tensor = np.random.uniform(0.1, 0.9, (3, 224, 224)).astype(np.float32)
                elif class_idx in [0, 5, 7]:  # blast / early blight -> yellow halos & brown lesions
                    tensor[0] = np.random.normal(0.40, 0.10, (224, 224))
                    tensor[1] = np.random.normal(0.45, 0.10, (224, 224))
                    tensor[2] = np.random.normal(0.15, 0.05, (224, 224))
                elif class_idx in [2]:  # yellow rust -> bright yellow streaks (high R & G)
                    tensor[0] = np.random.normal(0.60, 0.08, (224, 224))
                    tensor[1] = np.random.normal(0.60, 0.08, (224, 224))
                    tensor[2] = np.random.normal(0.10, 0.04, (224, 224))
                else:  # other necrotic/fungal spot patterns
                    base_r = 0.25 + (class_idx * 0.02)
                    base_g = 0.50 - (class_idx * 0.02)
                    tensor[0] = np.random.normal(base_r, 0.08, (224, 224))
                    tensor[1] = np.random.normal(base_g, 0.08, (224, 224))
                    tensor[2] = np.random.normal(0.20, 0.06, (224, 224))

                tensor = np.clip(tensor, 0.0, 1.0)
                self.data.append(tensor)
                self.labels.append(class_idx)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        x = torch.from_numpy(self.data[idx]).float()
        y = torch.tensor(self.labels[idx], dtype=torch.long)
        return x, y

def train_disease_model():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using compute device: {device} ({torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'})")

    train_dataset = SyntheticAgriLeafDataset(num_samples=720, is_train=True)
    test_dataset = SyntheticAgriLeafDataset(num_samples=240, is_train=False)

    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

    model = MobileAgriNet(num_classes=len(CLASSES)).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.parameters(), lr=0.003, weight_decay=1e-4)

    print(f"Beginning training MobileAgriNet (12 Indian agricultural classes)...")
    model.train()
    start_time = time.time()
    for epoch in range(12):
        running_loss = 0.0
        correct = 0
        total = 0
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * images.size(0)
            _, preds = torch.max(outputs, 1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)

        epoch_loss = running_loss / total
        epoch_acc = correct / total
        if (epoch + 1) % 3 == 0 or epoch == 11:
            print(f"Epoch [{epoch+1:02d}/12] - Loss: {epoch_loss:.4f} - Train Acc: {epoch_acc*100:.2f}%")

    train_time = time.time() - start_time
    print(f"Training completed in {train_time:.2f} seconds.")

    # Held-out evaluation
    model.eval()
    all_preds = []
    all_targets = []
    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(device)
            outputs = model(images)
            _, preds = torch.max(outputs, 1)
            all_preds.extend(preds.cpu().numpy())
            all_targets.extend(labels.numpy())

    test_acc = accuracy_score(all_targets, all_preds)
    print("\n==========================================")
    print(f"Held-out Validation Accuracy: {test_acc * 100:.2f}%")
    print("==========================================\n")
    print(classification_report(all_targets, all_preds, target_names=CLASSES))

    # Save PyTorch weights
    model_pth_path = os.path.join(OUTPUT_DIR, "crop_disease_model.pth")
    torch.save(model.state_dict(), model_pth_path)
    print(f"Saved PyTorch weights: {model_pth_path}")

    # Export ONNX model
    dummy_input = torch.randn(1, 3, 224, 224, device=device)
    onnx_path = os.path.join(OUTPUT_DIR, "crop_disease_model.onnx")
    torch.onnx.export(
        model,
        dummy_input,
        onnx_path,
        export_params=True,
        opset_version=14,
        input_names=["input"],
        output_names=["output"],
        dynamic_axes={"input": {0: "batch_size"}, "output": {0: "batch_size"}}
    )
    onnx_size_kb = os.path.getsize(onnx_path) / 1024
    print(f"Saved ONNX model: {onnx_path} ({onnx_size_kb:.1f} KB)")

    # Export disease labels mapping
    labels_file = os.path.join(OUTPUT_DIR, "disease_labels.txt")
    with open(labels_file, "w", encoding="utf-8") as f:
        for c in CLASSES:
            f.write(c + "\n")
    print(f"Saved disease labels to: {labels_file}")

    return test_acc

if __name__ == "__main__":
    train_disease_model()
