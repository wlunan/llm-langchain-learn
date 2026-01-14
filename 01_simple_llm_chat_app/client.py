from langserve import RemoteRunnable

# 确保服务器已在运行（serve.py）
# 通过api的方式调用langchain, 并输出内容
remote_chain = RemoteRunnable("http://localhost:8000/chain/")
result = remote_chain.invoke({"language": "italian", "text": "hi"})
print(result)
