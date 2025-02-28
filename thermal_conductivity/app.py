from flask import Flask, request, jsonify, send_file, render_template
import numpy as np
import torch
import torch.nn as nn
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import io
import uuid

app = Flask(__name__)

path_to_model_pth = 'model/materials_model.pth'

# 載入 PyTorch 模型
class MyModel(nn.Module):
    def __init__(self):
        super(MyModel, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(2, 512),
            nn.ReLU(),
            nn.Linear(512, 1)
        )

    def forward(self, x):
        return self.model(x)

model = MyModel()
model.load_state_dict(torch.load(path_to_model_pth))
model.eval()  # 設定為評估模式

# 用於暫存圖片的字典
image_cache = {}

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/api/predict/', methods=['POST'])
def predict():
    data = request.get_json()
    print(f'Received data: {data}')

    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    model_name = data.get('Model')
    power_input = data.get('Power_Input')
    temperature = data.get('Temperature')

    if model_name is None or power_input is None or temperature is None:
        return jsonify({'error': 'Missing parameters'}), 400

    # 這裡直接使用 PyTorch 模型進行預測
    input_data = np.array([[temperature, power_input]], dtype=np.float32)

    mean = np.array([25.0, 100.0])  # 這是虛擬的數值
    std = np.array([5.0, 20.0])  # 這是虛擬的數值

    # 手動標準化數據，先不考慮實際狀況，純展示用
    input_data_scaled = (input_data - mean) / std

    # 將標準化後的數據轉換為 PyTorch 張量
    input_tensor = torch.tensor(input_data_scaled, dtype=torch.float32)

    # 預測
    with torch.no_grad():
        predicted_thermal_conductivity = model(input_tensor).item()

    # 後處理：確保預測值非負
    predicted_thermal_conductivity = max(predicted_thermal_conductivity, 0)

    # 將預測值轉換為 Python 內置類型（例如 float）
    predicted_value = float(predicted_thermal_conductivity)

    return jsonify({'predicted_value': predicted_value})

@app.route('/api/image/<image_id>')
def get_image(image_id):
    if image_id not in image_cache:
        return jsonify({'error': 'Image not found'}), 404

    img = image_cache.pop(image_id)
    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
