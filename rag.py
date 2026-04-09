from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from vector_stores import  VectorStoreServices
from langchain_community.embeddings import  DashScopeEmbeddings
import config_date as config
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi

class RagServices(object):
    def __init__(self):
        self.vector_store = VectorStoreServices(
            DashScopeEmbeddings(model= config.embedding_model)
        )
        self.prompt_template = ChatPromptTemplate.from_messages(
            config.prompt
        )
        self.chat_modle = ChatTongyi(model=config.chat_modle)
        self.chain = self.__get_chain()
    def __get_chain(self):
        """获取最终的执行链"""
        retriever = self.vector_store.get_retriever()


        chain = (
            {
                "question":RunnablePassthrough (),
                "context": retriever|(lambda docs: "\n\n".join([f"文档片段{doc.page_content}\n文档元数据{doc.metadata}\n" for doc in docs] ) if docs else "无相关参考资料")
            }
            | self.prompt_template
            | self.chat_modle
            | StrOutputParser()

        )
        return chain

#
# def format_documents(docs :list[Document]):
#     """格式化文档"""
#     if not docs:
#         return "无相关参考资料"
#     return "\n\n".join([f"文档片段{doc.page_content}\n文档元数据{doc.metadata}\n" for doc in docs])
