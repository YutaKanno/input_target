from streamlit_drawable_canvas import st_canvas
from PIL import Image
import streamlit as st
from io import BytesIO

def load_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return Image.open(BytesIO(data))



# === クリア状態制御用関数 ===
def clear_canvas():
    st.session_state.canvas_key = f"canvas_bg_{st.session_state.counter}"
    st.session_state.counter += 1

# === 描画キャンバス表示関数 ===
def plate(打席左右):
    x, y = 0, 0
    # セッションステート初期化
    if "canvas_key" not in st.session_state:
        st.session_state.canvas_key = "canvas_bg_0"
    if "counter" not in st.session_state:
        st.session_state.counter = 1

    # 背景画像読み込み
    if 打席左右 == '左':
        bg_image = load_image("Plate_L.png")
    else:
        bg_image = load_image("Plate_R.png")
    width, height = bg_image.size

    # Canvas 表示（keyにより強制再描画）
    canvas_result = st_canvas(
        fill_color="rgba(255, 255, 255, 0.0)",
        stroke_width=10,
        stroke_color="#000000",
        background_image=bg_image,
        update_streamlit=True,
        height=height,
        width=width,
        drawing_mode="point",
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