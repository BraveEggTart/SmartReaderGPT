import re
import logging
from typing import AsyncGenerator
from contextlib import asynccontextmanager

import docx
import openai
from fastapi import FastAPI, File, UploadFile
from fastapi.routing import APIRoute

from middlewares import make_middlewares
from schemas import Success, Fail
from config import settings

# 设置日志Level
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

# 设置OpenAI API密钥
openai.api_key = settings.OPENAI_KEY
openai.api_base = settings.OPENAI_PROXY


def custom_generate_unique_id(route: APIRoute) -> str:
    """openapi operationID 命名规则转变
    由接口路由函数名 下划线转大驼峰小驼峰
    """
    operation_id = re.sub(
        '_([a-zA-Z])',
        lambda m: (m.group(1).upper()),
        route.name.lower()
    )
    return operation_id


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    yield


app = FastAPI(
    title=settings.TITLE,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    openapi_url="/openapi.json",
    middleware=make_middlewares(),
    generate_unique_id_function=custom_generate_unique_id,
    contact={
        "name": "Brave EggTart",
        "url": "https://just4dream.club",
        "email": "braveeggtart@gmail.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://github.com/BraveEggTart/SmartReaderGPT/blob/main/LICENSE",
    },
    lifespan=lifespan,
)


@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    
    # 判断文件类型
    if not file.filename.endswith('.docx'):
        return Fail(msg="Only docx files now. Other file type will come soon!")

    # 处理 Word 文档
    doc = docx.Document(file.file)
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])

    prompt = f"""
    你的任务是基于以下文档内容生成一个的简短摘要。

    请对三个反引号之间的评论文本进行概括，最多30个词汇
    ```{text}```
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    result = response['choices'][0]['message']['content']

    return Success(data=result)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=80,
        reload=True,
        lifespan="on",
    )
