from langchain_chroma import  Chroma
import config_date as config



class VectorStoreServices(object):
    def __init__(self, embedding):
        # 嵌入模型
        self.embedding = embedding
        self.vector_store = Chroma(
            collection_name=config.collection_name,
            embedding_function=self.embedding,
            persist_directory=config.persist_directory
        )
    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": config.search_kwargs})
