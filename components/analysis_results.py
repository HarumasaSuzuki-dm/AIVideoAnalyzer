import streamlit as st
import plotly.graph_objects as go

def display_analysis_results(report: dict):
    """Display analysis results in organized tabs."""
    tabs = st.tabs(["Summary", "Key Phrases", "Sentiment", "Full Text"])
    
    with tabs[0]:
        display_summary(report['summaries'])
    
    with tabs[1]:
        display_key_phrases(report['key_phrases'])
    
    with tabs[2]:
        display_sentiment(report['sentiment'])
    
    with tabs[3]:
        display_full_text(report['full_text'])

def display_summary(summaries: dict):
    """Display brief and detailed summaries."""
    st.subheader("Brief Summary")
    st.write(summaries['brief'])
    
    st.subheader("Detailed Summary")
    st.write(summaries['detailed'])

def display_key_phrases(phrases: list):
    """Display key phrases with explanations."""
    st.subheader("Key Phrases")
    for phrase in phrases:
        with st.expander(phrase['phrase']):
            st.write(phrase['explanation'])

def display_sentiment(sentiment: dict):
    """Display sentiment analysis with gauge charts."""
    st.subheader("Sentiment Analysis")
    
    for metric, value in sentiment.items():
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=value * 100,
            title={'text': metric.capitalize()},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={'axis': {'range': [0, 100]}}
        ))
        st.plotly_chart(fig, use_container_width=True)

def display_full_text(text: str):
    """Display full transcript text."""
    st.subheader("Full Interview Transcript")
    st.text_area("", text, height=400)
