import numpy as np
import torch
from torch.nn import Module
from yolov5.models.experimental import Ensemble
from yolov5.models.yolo import Model
from typing import Union

# 判定の処理を行うクラス
class HanteiController:
    model: Union[Module, Ensemble, Model]

    def __init__(self):
        self.model = torch.hub.load('.', 'custom', path='best.pt', source='local', device=torch.device('cpu'))

    def judge(self, frame: np.ndarray) -> str:
        self.model.conf = 0.5  # minimum confidence threshold
        results = self.model(frame, size=240)
        print(results)
        return ""
