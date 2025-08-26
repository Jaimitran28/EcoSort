import io
from PIL import Image
import torch
from torchvision import models, transforms
from torchvision.models import MobileNet_V2_Weights, ResNet18_Weights
from keywords import keyword_map, keyword_tips
import requests

# Load MobileNet
mobilenet = models.mobilenet_v2(weights=MobileNet_V2_Weights.DEFAULT)
mobilenet.eval()

# Load ResNet18
resnet = models.resnet18(weights=ResNet18_Weights.DEFAULT)
resnet.eval()

# Transform
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

# ImageNet labels
LABELS_URL = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
imagenet_labels = requests.get(LABELS_URL).text.splitlines()


def fallback_classify(file_storage):
    """Classify image using MobileNet first, fallback to ResNet if confidence is low,
       and select the top label with relevant disposal tips."""
    try:
        img_bytes = file_storage.read()
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        input_tensor = transform(img).unsqueeze(0)

        # --- MobileNet ---
        with torch.no_grad():
            outputs = mobilenet(input_tensor)
            probs = torch.nn.functional.softmax(outputs[0], dim=0)
            conf, idx = torch.max(probs, 0)

        # If confidence is low, fallback to ResNet
        if conf < 0.3:
            with torch.no_grad():
                outputs = resnet(input_tensor)
                probs = torch.nn.functional.softmax(outputs[0], dim=0)
                conf, idx = torch.max(probs, 0)

        # Top-5 labels
        top5_prob, top5_idx = torch.topk(probs, 5)
        top5_labels = [imagenet_labels[i].lower() for i in top5_idx]

        # Pick the label with the best available tips
        best_category = "unknown"
        best_tips = ["No tips available."]
        best_confidence = float(top5_prob[0])
        chosen_label = top5_labels[0]

        for lbl, p in zip(top5_labels, top5_prob):
            for keyword, cat in keyword_map.items():
                if keyword in lbl:
                    tips = keyword_tips.get(keyword, ["No tips available."])
                    if tips and tips != ["No tips available."]:
                        best_category = cat
                        best_tips = tips
                        best_confidence = float(p)
                        chosen_label = lbl
                        break
            if best_category != "unknown":
                break

        # Fallback if no keywords matched
        if best_category == "unknown":
            lbl = chosen_label
            if any(x in lbl for x in ["bottle", "can", "jar", "metal", "plastic", "glass", "paper"]):
                best_category = "recyclable"
                best_tips = ["Rinse before recycling.", "Separate caps.", "Do not mix with trash."]
            elif any(x in lbl for x in ["food", "banana", "apple", "leaf", "plant"]):
                best_category = "compostable"
                best_tips = ["Add to compost.", "Avoid meat/dairy.", "Chop large scraps."]
            else:
                best_category = "trash"
                best_tips = ["Dispose in trash.", "Do not burn.", "Keep in covered bin."]

        return {
            "category": best_category,
            "label": chosen_label,
            "confidence": best_confidence,
            "tips": best_tips,
            "top_labels": top5_labels
        }

    except Exception:
        return {
            "category": "unknown",
            "label": "error",
            "confidence": 0.0,
            "tips": ["Failed to process image."],
            "top_labels": []
        }
