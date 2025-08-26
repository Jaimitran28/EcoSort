# EcoSort — Smart Waste Classifier

EcoSort is a web application that helps you classify waste into **Recyclable**, **Compostable**, or **Trash**.  
You can upload an image of an item or describe it in text, and the system will use **AI (PyTorch models)** and rule-based logic to suggest the correct category along with **eco-friendly disposal tips**.

---

## 🚀 Features
- Upload an image or type an item name for classification.
- AI-powered image recognition (MobileNetV2, ResNet18).
- Rule-based fallback classifier for text inputs.
- Eco-friendly disposal tips for each category.
- Clean responsive UI with animations (Tailwind + custom CSS).
- Flask backend for lightweight deployment.

---

## 🛠️ Tech Stack
- **Backend**: Flask (Python)
- **ML Models**: PyTorch (MobileNetV2 + ResNet18)
- **Frontend**: Tailwind CSS, Custom Animations, Responsive Design
- **Database**: SQLite (for tips & categories)

---

## 📂 Project Structure
```
ecosort/
│── app.py                # Flask app entry point
│── models/
│   ├── classifier.py     # AI image/text classification logic
│   ├── fallback.py       # Rule-based classifier
│── templates/
│   └── base.html         # Base template with blocks
│── static/
│   ├── style.css         # Main styles
│   ├── responsive.css    # Responsive styles
│   ├── animations.css    # Animations
│   ├── animations.js     # Intro & transition animations
│   ├── script.js         # Main frontend logic
│   └── logo.png          # EcoSort logo
│── requirements.txt      # Python dependencies
│── README.md             # Project documentation
```

---

## ⚙️ Installation & Setup

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/ecosort.git
cd ecosort
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scriptsctivate     # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
python app.py
```
App will be available at: `http://127.0.0.1:5000`

---

## 📦 Deployment
For production deployment:
- Use **Gunicorn** or **uWSGI** with Nginx.
- Example:
```bash
pip install gunicorn
gunicorn -w 4 app:app
```

---

## 🌱 Example Usage
- Upload an image of a **plastic bottle** → Classified as **Recyclable**.
- Type **banana peel** → Classified as **Compostable** with disposal tips.
- Type **chip packet** → Classified as **Trash** with disposal tips.

---
