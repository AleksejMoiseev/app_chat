from adapters.storage import PythonStructRepository


user_storage = PythonStructRepository('users')
message_storage = PythonStructRepository('message')
chat_storage = PythonStructRepository('chat')
chat_member_storage = PythonStructRepository("chat_member")