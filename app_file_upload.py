import time

import streamlit as st
from knowledge_base import KnowledgeBaseServices

st.title("文件更新服务")

uploaded_file = st.file_uploader(
    "请上传txt文件",
    type = [ "txt"],
    accept_multiple_files= False
)


if "Knowledgebase" not in st.session_state:
    st.session_state.Knowledgebase = KnowledgeBaseServices()

if uploaded_file :
    file_name = uploaded_file.name
    file_type = uploaded_file.type
    file_size = uploaded_file.size / 1024
    st.subheader(f"文件名称：{file_name}")
    st.write(f"文件类型：{file_type}|文件大小：{file_size:.2f}KB")
    text = uploaded_file.read().decode("utf-8")
    # 显示文件解析
    with st.spinner("正在解析文件..."):
        time.sleep(1)
        ans =  st.session_state.Knowledgebase.upload_by_str(text, file_name)
        st.write(ans)