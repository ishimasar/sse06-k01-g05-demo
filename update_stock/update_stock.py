import json
import cv2
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt


pan_list = [
    "croissant",
    "cream-filled_roll",
    "white_bread",
    "anpan",
]


def main():
    img = cv2.imread("test_0.jpg")  # 入力画像
    dst = img.copy()  # 出力画像

    for pan in pan_list:
        template = cv2.imread(f"template/{pan}.jpg", )  # テンプレート画像
        
        # パン検出
        result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)

        # 類似度0.9以上を抽出
        ys, xs = np.where(result >= 0.9)
        rect_color = np.random.choice(range(256), size=3).tolist()
        
        # 重複検出を削除(ユークリッド距離30以下を間引き)
        p_list = [[xs[0], ys[0]]]
        for x, y in zip(xs, ys):
            is_append = True
            for p in p_list:
                a = np.array(p)
                b = np.array([x, y])
                if np.linalg.norm(a - b) < 30:
                    is_append = False
            if is_append:
                p_list.append([x, y])
        
        # 検出結果を描画
        for p in p_list:
            cv2.rectangle(dst, (p[0], p[1]), (p[0] + template.shape[1], p[1] + template.shape[0]), color=rect_color, thickness=1)
        
        # jsonに在庫情報を反映
        try:
            update_stock("../calculate/bread_inventory.json", pan, len(p_list))
        except Exception as err:
            print(err)
            print(f"failed to update {pan}.")
    
    cv2.imwrite("result.jpg", dst)


def update_stock(json_path, pan_name, stock):
    with Path(json_path).open() as f:
        inventory = json.load(f)

    for bread in inventory:
        if bread["bread_name"] == pan_name:
            bread["stock"] = stock
    
    with open(Path(json_path), "w") as f:
        json.dump(inventory, f, indent=4)


if __name__ == "__main__":
    main()
