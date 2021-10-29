# ライブラリのインポート
import cv2
import numpy as np
import glob

cap = cv2.VideoCapture(0)

# ノイズ除去のためのカーネルの定義
kernel = np.ones((5, 5), np.uint8)

# フォルダにある画像の枚数を取得
data = glob.glob("./data/*.jpg")
n_data = len(data)
# 実行
while True:

    # Webカメラのフレーム取得
    ret, frame = cap.read()


    """
    2-rgb2hue.pyと同じ方法で特定の色抽出
    """
    # 画像をRGBからHSVに変換
    
    frame = np.clip(1.0 * frame + 50.0, 0, 255).astype(np.uint8)
    
    cv2.imshow("camera", frame)
        
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    
    


    # HSVによる上限、下限の設定　 ([Hue, Saturation, Value])
    hsvLower = np.array([-10, 60, 60])  # 下限
    hsvUpper = np.array([40, 255, 255])  # 上限
    
        # HSVからマスクを作成
    hsv_mask = cv2.inRange(hsv, hsvLower, hsvUpper)


            # 白色領域のノイズを除去する
    hsv_mask = cv2.erode(hsv_mask, kernel)  # 収縮処理


    hsv_mask = cv2.dilate(hsv_mask, kernel)  # 膨張処理

    cv2.imshow("output", hsv_mask)
    
    src = cv2.cvtColor(hsv_mask, cv2.COLOR_GRAY2BGR)

    # ラベリング処理
    nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(hsv_mask)
    
 # 領域(stats[:, 4])が3つ以上ある場合(そのうち1つは背景)だけ処理
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
            # 長方形以外を使いたい時はURL参照→(http://labs.eecs.tottori-u.ac.jp/sd/Member/oyamada/OpenCV/html/py_tutorials/py_gui/py_drawing_functions/py_drawing_functions.html)
            cv2.rectangle(src, (x0, y0), (x1, y1), (0, 0, 255), 5)


    # 結果画像の表示
    cv2.imshow("output", src)
    

    
    
        # 終了オプション
    k = cv2.waitKey(1)
    
    
    if k == ord("s"):
        cv2.imwrite(
                f"./data/{n_data}.jpg", frame[y0 : y1 + 1, x0 : x1 + 1]
            )

        n_data += 1
        
    if k == ord("q"):
        break
    
cap.release()
cv2.destroyAllWindows()