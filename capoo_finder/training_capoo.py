from ultralytics import YOLO
import time

FILEANME_MODEL = "yolo11n.pt"
FILENAME_CONFIGS = "configs/yolo11n_capoo.yaml"
PROJECT_NAME = "capoo"
LEARNING_RATE = 0.001
EPOCHS_SET = 100
IMG_RESIZE = 320
OUTPUT_FOLDER = "capoo_dogdog_training"
# Load a model
model = YOLO(FILEANME_MODEL)  # load a pretrained model (recommended for training)

# Train the model with MPS
# results = model.train(data="configs/yolo11n_capoo.yaml", epochs=100, imgsz=320, device="mps")
start_time = time.time()
results = model.train(
    data=FILENAME_CONFIGS, 
    epochs=EPOCHS_SET, 
    imgsz=320, 
    device="mps", 
    project=PROJECT_NAME, 
    lr0=LEARNING_RATE,
    name=OUTPUT_FOLDER
)

end_time = time.time()
elapsed_time = end_time - start_time
print(f"物體偵測訓練耗時: {round(elapsed_time, 2)} 秒")