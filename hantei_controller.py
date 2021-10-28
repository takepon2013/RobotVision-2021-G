import numpy as np

# 判定の処理を行うクラス
class HanteiController:

    # 画面に表示する文字列
    display_str = "Please Janken."

    # クラス名とIDの組み合わせ
    class_name = None
    LABEL2CLS = {0: "rock", 1: "scissors", 2: "paper"}

    def judge(self, frame: np.ndarray) -> str:
        model =
        model.conf = 0.5  # minimum confidence threshold
        results = model(frame, size=240)
        print(results)
        return ""
