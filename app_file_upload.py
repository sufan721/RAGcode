import pdfplumber
from docx import Document
from io import BytesIO

import streamlit as st
from knowledge_base import KnowledgeBaseServices

def extract_text_from_file(uploaded_file):
    """根据文件类型直接提取文本内容"""
    file_name = uploaded_file.name

    if file_name.endswith('.txt'):
        return uploaded_file.read().decode("utf-8")

    elif file_name.endswith('.pdf'):
        with pdfplumber.open(BytesIO(uploaded_file.read())) as pdf:
            return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

    elif file_name.endswith('.docx'):
        doc = Document(BytesIO(uploaded_file.read()))
        return "\n".join([para.text for para in doc.paragraphs])

    return None


st.title("RAG 知识库上传服务")

# 1. 扩展支持的文件类型
uploaded_file = st.file_uploader(
    "上传文档 (支持 txt, pdf, docx)",
    type=["txt", "pdf", "docx"]
)

if "Knowledgebase" not in st.session_state:
    st.session_state.Knowledgebase = KnowledgeBaseServices()

if uploaded_file:
    with st.spinner(f"正在解析 {uploaded_file.name}..."):
        # 2. 直接获取文本内容，无需本地 batch_convert 脚本
        text = extract_text_from_file(uploaded_file)

        if text:
            # 3. 直接上传到你的 RAG 后端
            ans = st.session_state.Knowledgebase.upload_by_str(text, uploaded_file.name)
            st.success(f"解析成功！后端响应：{ans}")
            st.text_area("预览提取的内容 (前500字):", text[:500], height=200)
        else:
            st.error("文件内容为空或解析失败")
