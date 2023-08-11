from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from PIL import Image
import torch
import torchvision.transforms as transforms
import torchvision.models as models
import torch.nn as nn
import os
\

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images/'
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = models.resnet50(pretrained=False)
model.fc = nn.Linear(model.fc.in_features, 6)
state_dict = torch.load("resnet52.pth", map_location=torch.device('cpu'))
model.load_state_dict(state_dict)
model.eval()
@app.route('/')
def main():
    return render_template('index.html')
@app.route('/talk')
def talk():
  return render_template("talk.html")
@app.route('/us')
def us():
    return render_template("us.html")
@app.route("/product")
def product():
    return render_template("product.html")

def preprocess_image(image_path):
    model.to(device)
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    image = Image.open(image_path).convert('RGB')
    input_img = transform(image)
    input_img_data = input_img.unsqueeze(0)
    input_batch = input_img_data.to(device)
    model.eval()
    with torch.no_grad():
        output = model(input_batch)
    probabilities = torch.nn.functional.softmax(output[0], dim=0)
    #predicted_class = torch.argmax(probabilities).item()
    values, indices = probabilities.topk(3)

    output_ans = []
    class_names = ['Brazil', 'Canada', 'Finland', 'France', 'Japan']

    for i in range(3):
        output_ans.append(class_names[indices[i]])
        output_ans.append(round(float(probabilities[indices[i]])*100, 2))
    return output_ans
    #confidence = probabilities[predicted_class].item()
    
    #return f"{class_names[predicted_class]}: {round(float(confidence)*100, 2)}%"
    #return {class_names[i]: round(float(probabilities[i])*100, 2) for i in range(5)}

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'no file'}), 400
    file = request.files['file']
    filename = secure_filename(file.filename)
    
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    fp = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    print(fp)
    result = preprocess_image(fp)
    return render_template("result.html", name = result, img = file.filename)

if __name__ == '__main__':
    app.run(debug=True)
