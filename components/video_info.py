import streamlit as st

def display_video_info(video_info: dict):
    """動画情報セクションの表示"""
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image(video_info['thumbnail'], use_container_width=True)
    
    with col2:
        st.subheader("動画の詳細")
        st.write(f"**タイトル:** {video_info['title']}")
        st.write(f"**再生時間:** {video_info['duration']}")
