# 使用官方的 Python 镜像作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制 pyproject.toml 和 poetry.lock 文件到工作目录
COPY pyproject.toml poetry.lock* /app/

# 安装 Poetry
RUN pip install poetry

# 安装项目依赖
RUN poetry install --no-root

# 复制项目文件到工作目录
COPY . /app

# 暴露 FastAPI 默认端口
EXPOSE 8000

# 启动 FastAPI 应用
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]