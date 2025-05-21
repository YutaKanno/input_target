import streamlit as st
import streamlit.components.v1 as components
import plate
import matplotlib.pyplot as plt
import pandas as pd
#from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import base64
import cv2
import io

st.set_page_config(
        page_title="Input Target App",
        page_icon="📝",
        layout="wide",  # ウィンドウサイズに合わせて広く表示
    )
hide_all_style = """
    <style>
    /* 上部のメニュー・フッター */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 一番上の余白を消す */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
    }
    </style>
"""
st.markdown(hide_all_style, unsafe_allow_html=True)



data = pd.read_csv('test_data.csv', encoding='cp932')
data['守備チーム'] = np.where(data['表.裏'] == '表', data['後攻チーム'], data['先攻チーム'])
df = data[data['守備チーム'] == '東海大学']



with open("Plate_R.txt", "r", encoding="utf-8") as f:
    plate_R = f.read()
with open("Plate_L.txt", "r", encoding="utf-8") as f:
    plate_L = f.read()

def base64_to_np(base64_str):
    img_data = base64.b64decode(base64_str)
    img_array = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)  # BGR形式で読み込み
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # RGBに変換
    return img



col01, col02, col03 = st.columns(3)

with col01:
    selected_name = st.selectbox('p_name', df['投手氏名'].unique(), key='selected_name')

with col02:
    name_fil = df[df['投手氏名'] == selected_name]
    selected_date = st.selectbox('date', name_fil['試合日時'].unique(), key='selected_date')
with col03:
    date_fil = name_fil[name_fil['試合日時'] == selected_date]
    selected_inning = st.selectbox('inning', date_fil['回'].unique(), key='selected_inning')
    

# フィルタリング
df_fil1 = name_fil[name_fil['回'] == selected_inning]
df_fil = df_fil1[(df_fil1['target_x'].isin(['0', 0])) & (df_fil1['target_z'].isin(['0', 0]))]

# === indexのリセット判定 ===
if (
    "last_selected_name" not in st.session_state or
    "last_selected_date" not in st.session_state or
    "last_selected_inning" not in st.session_state or
    st.session_state.last_selected_name != selected_name or
    st.session_state.last_selected_date != selected_date or
    st.session_state.last_selected_inning != selected_inning
):
    st.session_state.index = 0
    st.session_state.last_selected_name = selected_name
    st.session_state.last_selected_date = selected_date
    st.session_state.last_selected_inning = selected_inning



def return_lists(df_fil):
    b_name_list = df_fil['打者氏名'].tolist()
    b_lr_list = df_fil['打席左右'].tolist()
    url_list = df_fil['URL'].tolist()
    plate_x_list = df_fil['コースX'].tolist()
    plate_z_list = df_fil['コースY'].tolist()
    pt_list = df_fil['球種'].tolist()
    speed_list = df_fil['球速'].tolist()
    result_list = df_fil['打撃結果'].tolist()
    inning_list = df_fil['回'].tolist()
    s_list = df_fil['S'].tolist()
    b_list = df_fil['B'].tolist()
    o_list = df_fil['アウト'].tolist()
    start_list = df_fil['start_tag_sec'].tolist()
    target_x_list = df_fil['target_x'].tolist()
    target_z_list = df_fil['target_z'].tolist()

    second = int(start_list[st.session_state["index"]])
    URL = url_list[st.session_state["index"]]

    youtube_url = f'''
    <iframe width="650" height="415" 
    src="{URL}&start={second}&autoplay=1&mute=1" 
    title="YouTube video player" frameborder="0" 
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
    referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
    '''
    
    point = (400*plate_x_list[st.session_state["index"]]/261, 400-400*plate_z_list[st.session_state["index"]]/261)

    if b_lr_list[st.session_state['index']] == '右':
        bg_image = base64_to_np(plate_R)
    else:
        bg_image = base64_to_np(plate_L)
        
    return b_name_list, b_lr_list, plate_x_list, plate_z_list, pt_list, speed_list, result_list, inning_list, s_list, b_list, o_list, target_x_list, target_z_list, youtube_url, point, bg_image






    









tab1, tab2 = st.tabs(['input target', 'show data'])
with tab1:
    b_name_list, b_lr_list, plate_x_list, plate_z_list, pt_list, speed_list, result_list, inning_list, s_list, b_list, o_list, target_x_list, target_z_list, youtube_url, point, bg_image = return_lists(df_fil)
    col1, col2, col3 = st.columns([8,4,5])
    with col1:
        components.html(youtube_url, height=500)
    with col2:
        fig, ax = plt.subplots()
        ax.imshow(bg_image, extent=[0, 400, 0, 400])
        ax.scatter(*point, color='red', zorder=15)
        ax.set_xlim(0, 400)
        ax.set_ylim(0, 400)
        ax.set_aspect('equal')
        ax.set_xlim(2,398)
        ax.set_ylim(2,398)
        ax.axis('off')
        
        st.pyplot(fig)
        st.write(f'### vs {b_name_list[st.session_state["index"]]}')
        st.write(f'{round(inning_list[st.session_state["index"]])}回 {round(o_list[st.session_state["index"]])}死')
        st.write(f'S: {"●"*int(s_list[st.session_state["index"]])}')
        st.write(f'B: {"●"*int(b_list[st.session_state["index"]])}')
        st.write(f'**{result_list[st.session_state["index"]]} {pt_list[st.session_state["index"]]}({round(speed_list[st.session_state["index"]])}km/h)**')
        
    with col3:
        target_x, target_z = plate.plate(bg_image)
        st.write('#### 目標位置を入力してください')
        
        # 入力値をdf_filに反映
        df_fil.at[df_fil.index[st.session_state["index"]], 'target_x'] = target_x
        df_fil.at[df_fil.index[st.session_state["index"]], 'target_z'] = target_z

        # 元データdataにも反映（indexで直接指定）
        data.at[df_fil.index[st.session_state["index"]], 'target_x'] = target_x
        data.at[df_fil.index[st.session_state["index"]], 'target_z'] = target_z

        if st.button('次のプレーへ'):
            plate.clear_canvas()
            data.to_csv('test_data.csv', encoding='cp932', index=False)
            if st.session_state["index"] < len(pt_list) - 1:
                st.session_state["index"] += 1
                st.rerun()



with tab2:
    b_name_list, b_lr_list, plate_x_list, plate_z_list, pt_list, speed_list, result_list, inning_list, s_list, b_list, o_list, target_x_list, target_z_list, youtube_url, point, bg_image = return_lists(df_fil1)
    col1, col2, col3 = st.columns([4,2,2])
    with col1:
        components.html(youtube_url, height=500)
    with col2:
        fig, ax = plt.subplots()
        ax.imshow(bg_image, extent=[0, 400, 0, 400])
        ax.scatter(*point, color='red', zorder=15)
        ax.scatter(
            target_x_list[st.session_state["index"]],
            target_z_list[st.session_state["index"]],
            color='blue',
            zorder=15
        )
        ax.text(target_x_list[st.session_state["index"]],
                target_z_list[st.session_state["index"]] - 20,
                'target', color='blue', ha='center', fontsize=10, zorder=20) 
        ax.set_xlim(0, 400)
        ax.set_ylim(0, 400)
        ax.set_aspect('equal')
        ax.set_xlim(5,395)
        ax.set_ylim(5,395)
        ax.axis('off')
        
        st.pyplot(fig)
        st.write(f'### vs {b_name_list[st.session_state["index"]]}')
        st.write(f'{round(inning_list[st.session_state["index"]])}回 {round(o_list[st.session_state["index"]])}死')
        st.write(f'S: {"●"*int(s_list[st.session_state["index"]])}')
        st.write(f'B: {"●"*int(b_list[st.session_state["index"]])}')
        st.write(f'**{result_list[st.session_state["index"]]} {pt_list[st.session_state["index"]]}({round(speed_list[st.session_state["index"]])}km/h)**')
        
    with col3:
        if st.button('NEXT'):
            if st.session_state["index"] < len(pt_list) - 1:
                st.session_state["index"] += 1
                st.rerun()
        if st.button('BACK'):
            if st.session_state["index"] >= 1:
                st.session_state["index"] -= 1
                st.rerun()
        if st.button('INNING TOP'):
            st.session_state["index"] = 0
            st.rerun()        
        
    
    