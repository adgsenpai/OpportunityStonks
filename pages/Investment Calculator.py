import streamlit as st

# hide made with streamlit
hide_streamlit_style = """
			<style>
			#MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
			</style>
			"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
