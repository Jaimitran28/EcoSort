# classifier.py
import torch
import torchvision.transforms as transforms
from PIL import Image
import io
from keywords import keyword_map
from torchvision import models
from torchvision.models import MobileNet_V2_Weights, ResNet18_Weights
import requests

# ---------------------------
# Load Models
# ---------------------------
mobilenet = models.mobilenet_v2(weights=MobileNet_V2_Weights.DEFAULT)
mobilenet.eval()

resnet = models.resnet18(weights=ResNet18_Weights.DEFAULT)
resnet.eval()

# ---------------------------
# Image Preprocessing
# ---------------------------
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

# ---------------------------
# Load ImageNet labels
# ---------------------------
LABELS_URL = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
imagenet_labels = requests.get(LABELS_URL).text.splitlines()

# ---------------------------
# Map text/label to category
# ---------------------------
def map_to_category(text: str) -> str:
    text = text.lower()
    for keyword, category in keyword_map.items():
        if keyword in text:
            return category
    return "unknown"

# ---------------------------
# Image classifier
# ---------------------------
def classify_image(file):
    """Classify uploaded image using MobileNet, fallback to ResNet."""
    try:
        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes)).convert('RGB')
        input_tensor = preprocess(img).unsqueeze(0)

        # Stage 1: MobileNet
        with torch.no_grad():
            outputs = mobilenet(input_tensor)
            probs = torch.nn.functional.softmax(outputs[0], dim=0)
            conf, idx = torch.max(probs, 0)

        # Stage 2: fallback to ResNet if confidence is low
        if conf < 0.3:
            with torch.no_grad():
                outputs = resnet(input_tensor)
                probs = torch.nn.functional.softmax(outputs[0], dim=0)
                conf, idx = torch.max(probs, 0)

        # Top-5 predictions
        top5_idx = torch.topk(probs, 5).indices.tolist()
        top5_labels = [imagenet_labels[i].lower() for i in top5_idx]

        # Map to category using keyword_map
        category = "unknown"
        for lbl in top5_labels:
            cat = map_to_category(lbl)
            if cat != "unknown":
                category = cat
                break

        return category, float(conf), top5_labels

    except Exception:
        return "unknown", 0.0, []

# ---------------------------
# Text classifier
# ---------------------------
def classify_text(text):
    """Classify text input using keyword_map."""
    text = text.lower()
    category = map_to_category(text)

    if category == "unknown":
        return "unknown", 0.5, []
    else:
        return category, 0.9, [category]
