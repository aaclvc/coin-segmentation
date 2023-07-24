'''
CLI
Train:
yolo segment train data="./datasets/coin-segmentation/dataset.yaml" model=yolov8n-seg.pt epochs=150 imgsz=640 batch=8 device=mps

Predict:

yolo segment predict model=runs/segment/train2/weights/best.pt source=1 show=True

Validate:
yolo segment val model=runs/segment/train2/weights/best.pt data=dataset.yaml
'''

from ultralytics import YOLO

# Load a model
model = YOLO('yolov8n-seg.pt')  # load a pretrained model (recommended for training)

# Train the model
model.train(data='dataset.yaml', epochs=150, imgsz=640, batch=8, device='mps')
