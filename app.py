
import streamlit as st
st.set_page_config(page_title="QuLab", layout="wide")
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("QuLab")
st.divider()
st.markdown("""
In this lab, we will explore the Crypto Operational Loss Mitigation Simulator.
This application provides an interactive platform for simulating operational loss events within a hypothetical cryptocurrency exchange environment. Its primary objective is to demonstrate and analyze the financial impact of different insurance-like mitigation strategies, such as self-insurance funds or traditional excess-of-loss policies.

formulae, explanations, tables, etc.
""")
# Your code starts here
page = st.sidebar.selectbox(label="Navigation", options=["Simulator", "Explanation", "About"])
if page == "Simulator":
    from application_pages.page1 import run_page1
    run_page1()
elif page == "Explanation":
    from application_pages.page2 import run_page2
    run_page2()
elif page == "About":
    from application_pages.page3 import run_page3
    run_page3()
# Your code ends
