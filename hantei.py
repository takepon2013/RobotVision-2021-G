import cv2
import numpy as np
from skimage.feature import hog
from sklearn.neighbors import NearestNeighbors

cap = cv2.VideoCapture(0)

# 特徴量の読み込み
features = np.load("./data/features.npy")
labels = np.load("./data/labels.npy")

# 最近傍探索のモデルを定義
model = NearestNeighbors(n_neighbors=1).fit(features)

# スクショしたかどうかを保存する変数 (まだ撮っていないのでFalse)
screenshot = False
# スクショを保存する変数
photo = None

# ノイズ除去のためのカーネルの定義
kernel = np.ones((5, 5), np.uint8)

# 画面に表示する文字列
display_str = "Please Janken."

# クラス名とIDの組み合わせ
class_name = None
LABEL2CLS = {0: "rock", 1: "scissors", 2: "paper"}

# 実行
while True:
    # Webカメラのフレーム取得
    ret, frame = cap.read()

    src = frame.copy()

    # 今映っている人のクラスを表示
    # putText(描画画像、 書き込む文字列、 書き込む座標、 フォント、 サイズ、 色、 太さ)
    if class_name is not None:
        display_str = f"class: {class_name}"

    cv2.putText(
        src, display_str, (30, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 1,
    )

    cv2.imshow("camera", src)

    # キーボードの入力の受付
    k = cv2.waitKey(1)

    frame = np.clip(1.0 * frame + 50.0, 0, 255).astype(np.uint8)


    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # HSVによる上限、下限の設定　 ([Hue, Saturation, Value])
    hsvLower = np.array([-10, 60, 60])  # 下限
    hsvUpper = np.array([40, 255, 255])  # 上限

    # HSVからマスクを作成
    hsv_mask = cv2.inRange(hsv, hsvLower, hsvUpper)

    # 白色領域のノイズを除去する
    hsv_mask = cv2.erode(hsv_mask, kernel)  # 収縮処理


    hsv_mask = cv2.dilate(hsv_mask, kernel)  # 膨張処理

    nlabels, labels2, stats, centroids = cv2.connectedComponentsWithStats(hsv_mask)

    if nlabels >= 3:
        # 面積でソート(今回は面積が上位２つの領域を利用)
        top_idx = stats[:, 4].argsort()[-2:-1]

        # 各領域において...
        for i in top_idx:

            # ターミナル上に詳細表示
            print(
                "[x0: {}, y0: {}, x幅: {}, y幅: {}, 面積: {}]".format(
                    stats[i, 0], stats[i, 1], stats[i, 2], stats[i, 3], stats[i, 4]
                )
            )

            # 領域の外接矩形の角座標を入手
            x0 = stats[i, 0]
            y0 = stats[i, 1]
            x1 = x0 + stats[i, 2]
            y1 = y0 + stats[i, 3]
            # 長方形描画 (引数 : 描画画像、 長方形の左上角、 長方形の右下角、 色(BGR)、 線の太さ)

    # grayscaleに変換
    gray = cv2.cvtColor(
            src[y0 : y1 + 1, x0 : x1 + 1], cv2.COLOR_BGR2GRAY
        )

    # リサイズ (H, W) = (56, 56) ※要調整
    gray = cv2.resize(gray, (56, 84))

    cv2.imshow("gray", gray)
    # HOGによって特徴抽出
    feat = hog(gray)

    # 配列の形を変更 (56*56,) => (1, 56*56)
    # feat = feat.reshape(1, 56 * 56) と同じ
    feat = feat.reshape(1, -1)

    # 最近傍探索. 二重のリストで結果が返ってくる.
    distances, indices = model.kneighbors(feat)

    # 近かった特徴量のインデックス(indicies)をクラスのラベルに変換
    label = labels[indices[0][0]]
    class_name = LABEL2CLS[label]

    # 終了
    if k == ord("q"):
        break

