import os
import config_date as config
import hashlib
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import DashScopeEmbeddings
from datetime import datetime


def check_md5(md5str: str):
    """
    检查md5是否存在
    False 未处理 ， True 处理过
    """
    if not os.path.exists(config.date_path):
        os.mkdir(config.date_path)
    if not os.path.exists(config.md5_path):
        open(config.md5_path, "w", encoding="utf-8").close()
        return False
    with open(config.md5_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip() == md5str:
                return True
        return False


def save_md5(md5str: str):
    """
    保存md5
    """
    if check_md5(md5str):
        return
    with open(config.md5_path, "a", encoding="utf-8") as f:
        f.write(md5str + "\n")


def get_string_md5(input_str: str, encoding="utf-8"):
    # 将传入的字符串改为md5
    str_byte = input_str.encode(encoding)
    md5 = hashlib.md5(str_byte)
    return md5.hexdigest()


class KnowledgeBaseServices(object):
    def __init__(self):
        os.makedirs(config.persist_directory, exist_ok=True)

        self.chroma = Chroma(
            collection_name=config.collection_name,  # 数据库的名称
            embedding_function=DashScopeEmbeddings(model="text-embedding-v4"),
            persist_directory=config.persist_directory  # 数据库的文件夹
        )
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            separators=config.separators,
            length_function=len,

        )

    def upload_by_str(self, date: str, filename):
        # 将传入的字符串，进行向量化，存入向量数据库
        md5_hex = get_string_md5(date)
        if check_md5(md5_hex):
            return "[跳过]内容已存在于知识库中"
        if len(date) > config.max_spilt_char_number:
            knowledge_chunks: list[str] = self.spliter.split_text(date)
        else:
            knowledge_chunks: list[str] = [date]
        metadata = {
            "source": filename,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator" : "su_fan"

        }
        self.chroma.add_texts(
            texts=knowledge_chunks,
            metadatas=[metadata for _ in knowledge_chunks]
        )
        save_md5(md5_hex)
        return "[成功]内容已保存到知识库中"


# 测试类
if __name__ == '__main__':
    kbs = KnowledgeBaseServices()
    print(kbs.upload_by_str("张三是个法外狂徒，他总是被拿来做案例", "test.txt"))