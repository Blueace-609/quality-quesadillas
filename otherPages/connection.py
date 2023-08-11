from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from PIL import Image
import torch
import torchvision.transforms as transforms
import torchvision.models as models
import torch.nn as nn

app = Flask(__name__)

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = models.resnet50(pretrained=False)
model.fc = nn.Linear(model.fc.in_features, 6)
state_dict = torch.load("resnet52.pth", map_location=torch.device('cpu'))
model.load_state_dict(state_dict)
model.eval()
@app.route('/')
def main():
  return render_template("talk.html")
def preprocess_image(image_path):
    model.to(device)
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    image = Image.open(image_path)
    input_img = transform(image)
    input_img_data = input_img.unsqueeze(0)
    input_batch = input_img_data.to(device)
    model.eval()
    with torch.no_grad():
        output = model(input_batch)
    probabilities = torch.nn.functional.softmax(output[0], dim=0)
    class_names = ['Brazil', 'Canada', 'Finland', 'France', 'Japan']
    return {class_names[i]: round(float(probabilities[i])*100, 2) for i in range(5)}

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'no file'}), 400
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(filename)
    result = preprocess_image(filename)
    return render_template("result.html", name=result, img=filename)

if __name__ == '__main__':
    app.run(debug=True)
