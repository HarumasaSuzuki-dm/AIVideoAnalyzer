import streamlit as st

def display_video_info(video_info: dict):
    """Display video information section."""
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image(video_info['thumbnail'], use_column_width=True)
    
    with col2:
        st.subheader("Video Details")
        st.write(f"**Title:** {video_info['title']}")
        st.write(f"**Duration:** {video_info['duration']}")
