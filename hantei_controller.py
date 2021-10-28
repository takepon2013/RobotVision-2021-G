import numpy as np
import torch

# 判定の処理を行うクラス
class HanteiController:

    # 画面に表示する文字列
    display_str = "Please Janken."

    # クラス名とIDの組み合わせ
    class_name = None
    LABEL2CLS = {0: "rock", 1: "scissors", 2: "paper"}
    model: any

    def __init__(self):
        self.model = torch.hub.load('.', 'custom', path='best.pt', source='local')

    def judge(self, frame: np.ndarray) -> str:
        self.model.conf = 0.5  # minimum confidence threshold
        results = self.model(frame, size=240)
        print(results)
        return ""
