from streamlit_drawable_canvas import st_canvas
from PIL import Image
import streamlit as st
import cv2

# === クリア状態制御用関数 ===
def clear_canvas():
    st.session_state.canvas_key = f"canvas_bg_{st.session_state.counter}"
    st.session_state.counter += 1

# === 描画キャンバス表示関数 ===
def plate(bg_np_array):
    x, y = 0, 0
    # セッションステート初期化
    if "canvas_key" not in st.session_state:
        st.session_state.canvas_key = "canvas_bg_0"
    if "counter" not in st.session_state:
        st.session_state.counter = 1

     # NumPy配列（OpenCV画像） → RGB変換
    rgb_img = cv2.cvtColor(bg_np_array, cv2.COLOR_BGR2RGB)

    # Pillow画像オブジェクトに変換（これだけは必要）
    image = Image.fromarray(rgb_img)

    # Canvas
    canvas_result = st_canvas(
        fill_color="rgba(255, 255, 255, 0.0)",
        stroke_width=10,
        stroke_color="#000000",
        background_image=image,
        update_streamlit=True,
        height=400,
        width=400,
        drawing_mode="freedraw",
        key=st.session_state.canvas_key
    )


    # 結果処理
    if canvas_result.json_data is not None:
        objects = canvas_result.json_data["objects"]
        if objects:
            last_obj = objects[-1]
            x = round(263*last_obj["left"] / 400, 1)
            y = round(263*last_obj["top"] /400, 1)
            return x, y
    return x, y