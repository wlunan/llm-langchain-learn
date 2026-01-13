from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langserve import add_routes
import os
# 1. Create prompt template
# system_template = "Translate the following into {language}:"
# prompt_template = ChatPromptTemplate.from_messages([
#     ('system', system_template),
#     ('user', '{text}')
# ])

# system_template 作为给模型的指令，告诉模型只计算数学公式
system_template = "计算以下的数学公式,对其他内容不进行计算,提醒用户只接受数学公式计算:"
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', '{math_expression}') # {math_expression}在前端会被渲染一个输入框
])

# 2. Create model
model = ChatOpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.environ["OPENAI_API_KEY"],
    model="qwen-plus"
)

# 3. Create parser
parser = StrOutputParser()

# 4. Create chain
chain = prompt_template | model | parser


# 4. App definition
app = FastAPI(
  title="LangChain Server",
  version="1.0",
  description="A simple API server using LangChain's Runnable interfaces",
)

# 5. Adding chain route
add_routes(
    app,
    chain,
    path="/chain",
)

if __name__ == "__main__":
    import uvicorn
    # http://localhost:8000/chain/playground/
    uvicorn.run(app, host="localhost", port=8000)