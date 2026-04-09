
md5_path = "./date/md5.text" #存储MD5文件的路径
date_path = "./date" #存储所有数据的文件夹


collection_name= "rag" # 数据库的名称
persist_directory = "./chroma_db"  # 数据库的文件夹


chunk_size= 1000
chunk_overlap = 100
separators = ["\n\n", "\n", ".", "?", "!", "。", "？","！"," ",""] #文本分隔符
max_spilt_char_number = 1000 # 文本最大长度


search_kwargs=  2 # 向量库匹配 每次返回的文件数量

embedding_model = "text-embedding-v4"
chat_modle = "qwen3-max"

prompt = [
    ("system", "以我提供的已知参考资料为主，简洁和专业的回答用户我问题。参考资料{context}"),
   ( "user","请根据提供的上下文，回答问题：{question}")
]
