import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageDraw
from io import BytesIO  # Base64エンコードのためにBytesIOをインポート

# === クリア状態制御用関数 ===
def clear_canvas():
    st.session_state.canvas_key = f"canvas_{st.session_state.counter}"
    st.session_state.counter += 1

# === 四角形付きの白い背景画像を生成 ===
def create_white_canvas_with_box():
    width, height = 400, 400
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    # 黒の枠線（座標に注意：順番で自動的に閉じる）
    draw.rectangle([80, 80, 320, 320], outline="black", width=3)
    return image

# === 描画キャンバス表示関数 ===
def plate():
    x, y = 0, 0

    if "canvas_key" not in st.session_state:
        st.session_state.canvas_key = "canvas_0"
    if "counter" not in st.session_state:
        st.session_state.counter = 1

    bg_image = create_white_canvas_with_box()

    # PIL ImageをBytesIOに保存し、それをst_canvasに渡す
    img_bytes = BytesIO()
    bg_image.save(img_bytes, format="PNG")  # PNG形式で保存
    img_bytes.seek(0)  # ファイルの先頭に移動

    canvas_result = st_canvas(
        fill_color="rgba(255, 255, 255, 0.0)",
        stroke_width=10,
        stroke_color="#ff0000",
        background_image=Image.open(img_bytes),  # BytesIOから再度PIL Imageとして読み込む
        update_streamlit=True,
        height=400,
        width=400,
        drawing_mode="point",
        key=st.session_state.canvas_key
    )

    if canvas_result.json_data is not None:
        objects = canvas_result.json_data["objects"]
        if objects:
            last_obj = objects[-1]
            x = round(263 * last_obj["left"] / 400, 1)
            y = round(263 * last_obj["top"] / 400, 1)
            return x, y

    return x, y
