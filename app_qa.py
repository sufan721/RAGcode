import streamlit as st
from app_file_upload import extract_text_from_file
from knowledge_base import KnowledgeBaseServices
from rag import RagServices
import config_date as config

st.header("RAG实践")


if "rag" not in st.session_state:
    st.session_state.rag = RagServices()
if "message" not in st.session_state:
    st.session_state.message = []
if "Knowledgebase" not in st.session_state:
    st.session_state.Knowledgebase = KnowledgeBaseServices()


for chunk in st.session_state.message:
    st.chat_message(chunk["role"]).write(chunk["content"])

with st.sidebar:
    st.title("📚 知识库管理")
    st.info("上传文档后，系统将自动解析并更新 RAG 知识库。")
    uploaded_file = st.file_uploader(
        "上传文档 (支持 txt, pdf, docx)",
        type=["txt", "pdf", "docx"]
    )

    if uploaded_file:
        with st.spinner(f"正在解析 {uploaded_file.name}..."):
            text = extract_text_from_file(uploaded_file)
            if text:
                ans = st.session_state.Knowledgebase.upload_by_str(text, uploaded_file.name)
                st.success(f"解析成功！后端响应：{ans}")
            else:
                st.error("文件内容为空或解析失败")



format = st.chat_input("请问您的问题")


if format:
    st.chat_message("user").write(format)
    st.session_state.message.append({"role": "user", "content": format})
    with st.spinner("思考中..."):
        response = st.session_state.rag.chain.stream({"input":  format},config.session_confing)
        st.chat_message("assistant").write_stream(response)
    st.session_state.message.append({"role": "assistant", "content": response})






