import cv2
import pandas as pd
import math
start_tag_list = [0]
duration_list = [0]
sum_sec = 0
last_video_num = 303

for i in range(last_video_num):
    video_path = f'test_video/ ({i+1}).mp4'

    # 動画を読み込む
    cap = cv2.VideoCapture(video_path)

    # フレーム数とFPSを取得
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    # 再生時間（秒）を計算
    duration = frame_count / fps if fps > 0 else 0
    cap.release()

    sum_sec = round(sum_sec + duration)
    sum_sec = math.floor(sum_sec)
    start_tag_list.append(sum_sec)
    duration_list.append(duration)

    print(f"{i+1}: 動画の長さ: {duration:.2f} 秒")

# データフレーム作成
df = pd.DataFrame({
    "duration_sec": duration_list,
    "start_tag_sec": start_tag_list
})

# CSV 出力
df.to_csv("video_duration_tags.csv", index=False)

print("CSVファイルに保存しました。")
