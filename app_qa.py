import streamlit as st
from rag import RagServices
import config_date as config

st.header("RAG实践")

if "rag" not in st.session_state:
    st.session_state.rag = RagServices()

if "message" not in st.session_state:
    st.session_state.message = []


format = st.chat_input("请问您的问题")

for chunk in st.session_state.message:
    st.chat_message(chunk["role"]).write(chunk["content"])


if format:
    st.chat_message("user").write(format)
    st.session_state.message.append({"role": "user", "content": format})
    with st.spinner("思考中..."):
        response = st.session_state.rag.chain.stream({"input":  format},config.session_confing)
        st.chat_message("assistant").write_stream(response)
    st.session_state.message.append({"role": "assistant", "content": response})




