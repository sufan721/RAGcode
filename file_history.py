import json
import os.path
from typing import Sequence
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict


def get_history(session_id: str) :
    return FileChatMessageHistory(session_id, "./chat_history")


class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self,session_id: str,  storage_path: str):
        self.session_id = session_id
        self.storage_path = storage_path

        self.file_path = os.path.join(self.storage_path,self.session_id)
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def add_message(self, message: BaseMessage) -> None:
        """添加单条消息"""
        all_messages = list(self.messages)
        all_messages.append(message)

        new_messages = [message_to_dict(msg) for msg in all_messages]
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(new_messages, f, ensure_ascii=False)


    def add_messages(self, message:Sequence[ BaseMessage ] ) -> None:
        all_messages = list(self.messages)
        all_messages.extend(message)


        new_messages = [message_to_dict( message) for message in all_messages]
        with open(self.file_path, "w",encoding="utf-8") as f:
            json.dump(new_messages, f)

    @ property
    def messages(self) -> list[BaseMessage]:
       try:
           with open(self.file_path, "r",encoding="utf-8") as f:
               messages = json.load(f)
               return messages_from_dict( messages)
       except FileNotFoundError:
           return  []

    def clear(self) -> None:
        with open(self.file_path, "w",encoding="utf-8") as f:
            json.dump([], f)