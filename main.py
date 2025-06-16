import streamlit as st
import streamlit.components.v1 as components
import input_target
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
import numpy as np
# ### 変更点 ###: SQLAlchemyライブラリをインポート
from sqlalchemy import create_engine, text

# --- データベース設定 ---
DB_FILE = 'baseball_data.db'
TABLE_NAME = 'pitch_data'
ENGINE = create_engine(f'sqlite:///{DB_FILE}')


st.set_page_config(
    page_title="Input Target App",
    page_icon="📝",
    layout="wide",
)
hide_all_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
    }
    </style>
"""
st.markdown(hide_all_style, unsafe_allow_html=True)


# ### 変更点 ###: CSVの代わりにデータベースからデータを読み込む
# index_col='id'で、データベースの'id'列をDataFrameのインデックスとして設定
data = pd.read_sql(TABLE_NAME, ENGINE, index_col='id')

data['守備チーム'] = np.where(data['表.裏'] == '表', data['後攻チーム'], data['先攻チーム'])
df = data[data['守備チーム'] == '筑波大学']

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
df_fil = df_fil1[(df_fil1['target_x'].isin(['0', 0, None, np.nan])) & (df_fil1['target_z'].isin(['0', 0, None, np.nan]))].copy()

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


def return_lists(df_to_process):
    b_name_list = df_to_process['打者氏名'].tolist()
    b_lr_list = df_to_process['打席左右'].tolist()
    url_list = df_to_process['URL'].tolist()
    plate_x_list = df_to_process['コースX'].tolist()
    plate_z_list = df_to_process['コースY'].tolist()
    pt_list = df_to_process['球種'].tolist()
    speed_list = df_to_process['球速'].tolist()
    result_list = df_to_process['打撃結果'].tolist()
    inning_list = df_to_process['回'].tolist()
    s_list = df_to_process['S'].tolist()
    b_list = df_to_process['B'].tolist()
    o_list = df_to_process['アウト'].tolist()
    start_list = df_to_process['start_tag_sec'].tolist()
    target_x_list = df_to_process['target_x'].tolist()
    target_z_list = df_to_process['target_z'].tolist()
    score_list = df_to_process['score'].tolist()
    comment_list = df_to_process['comment'].tolist()

    current_index = st.session_state.get("index", 0)

    second = int(start_list[current_index])
    URL = url_list[current_index]

    youtube_url = f'''
    <iframe width="100%" height="415" 
    src="{URL}&start={second}&autoplay=1&mute=1" 
    title="YouTube video player" frameborder="0" 
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
    referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
    '''

    point = (400 * plate_x_list[current_index] / 261, 400 - 400 * plate_z_list[current_index] / 261)

    if b_lr_list[current_index] == '右':
        bg_image = Image.open('Plate_R.png')
    else:
        bg_image = Image.open('Plate_L.png')

    return b_name_list, b_lr_list, plate_x_list, plate_z_list, pt_list, speed_list, result_list, inning_list, s_list, b_list, o_list, target_x_list, target_z_list, youtube_url, point, bg_image, score_list, comment_list


tab1, tab2, tab3 = st.tabs(['input target', 'show data', 'dataframe'])

with tab1:
    if not df_fil.empty:
        b_name_list, b_lr_list, plate_x_list, plate_z_list, pt_list, speed_list, result_list, inning_list, s_list, b_list, o_list, target_x_list, target_z_list, youtube_url, point, bg_image, score_list, comment_list = return_lists(df_fil)
        col1, col2, col3 = st.columns([4, 2, 3])
        with col1:
            components.html(youtube_url, height=500)
        with col2:
            fig, ax = plt.subplots()
            bg_image_np = np.array(bg_image)
            ax.imshow(bg_image_np, extent=[0, 400, 0, 400])
            ax.scatter(*point, color='red', zorder=15)
            ax.set_xlim(2, 398)
            ax.set_ylim(2, 398)
            ax.set_aspect('equal')
            ax.axis('off')

            st.pyplot(fig)
            st.write(f'### vs {b_name_list[st.session_state["index"]]}')
            st.write(f'{round(inning_list[st.session_state["index"]])}回 {round(o_list[st.session_state["index"]])}死')
            st.write(f'S: {"●" * int(s_list[st.session_state["index"]])}')
            st.write(f'B: {"●" * int(b_list[st.session_state["index"]])}')
            st.write(f'**{result_list[st.session_state["index"]]} {pt_list[st.session_state["index"]]}({round(speed_list[st.session_state["index"]])}km/h)**')

        with col3:
            target_x, target_z = input_target.plate(bg_image)

            options = ['-', 1, 2, 3, 4, 5]
            score = st.radio('自己評価', options, horizontal=True)
            comment = st.text_area('コメント')

            if st.button('次のプレーへ'):
                # ### 変更点 ###: データベースの特定の行を更新する
                record_id_to_update = df_fil.index[st.session_state["index"]]

                update_query = text(f"""
                    UPDATE {TABLE_NAME}
                    SET
                        target_x = :tx,
                        target_z = :tz,
                        score = :sc,
                        comment = :cm
                    WHERE
                        id = :rid
                """)

                with ENGINE.connect() as connection:
                    connection.execute(update_query, {
                        "tx": target_x,
                        "tz": target_z,
                        "sc": str(score),
                        "cm": comment,
                        "rid": int(record_id_to_update)
                    })
                    connection.commit()

                input_target.clear_canvas()
                st.rerun()

    else:
        st.success("🎉 このイニングの入力はすべて完了しました。")
        st.info("上のフィルターで別の投手・試合・イニングを選択するか、「show data」タブで結果を確認してください。")




with tab2:
    b_name_list, b_lr_list, plate_x_list, plate_z_list, pt_list, speed_list, result_list, inning_list, s_list, b_list, o_list, target_x_list, target_z_list, youtube_url, point, bg_image, score_list, comment_list = return_lists(df_fil1)
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
        st.write(f'**自己評価: {score_list[st.session_state["index"]]}点 / 5点**')
        st.write('**コメント:**')
        st.write(comment_list[st.session_state["index"]])
        
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
        
    
with tab3:
    st.dataframe(data)
