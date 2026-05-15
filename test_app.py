import streamlit as st

st.set_page_config(page_title="Test", page_icon="🧪")

st.title("Tabs + 按钮测试")

tabs = st.tabs(["Tab A", "Tab B", "Tab C"])

with tabs[0]:
    st.write("这是 Tab A")
    if st.button("按钮A", key="btn_a"):
        st.success("按钮A 被点击了！")

with tabs[1]:
    st.write("这是 Tab B")
    if st.button("按钮B", key="btn_b"):
        st.success("按钮B 被点击了！")

with tabs[2]:
    st.write("这是 Tab C")
    if st.button("按钮C", key="btn_c"):
        st.success("按钮C 被点击了！")
