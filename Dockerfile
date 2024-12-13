# 构建阶段
FROM python:3.11-slim AS builder

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.8.4 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# 将 poetry 和 venv 添加到 PATH
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# 安装系统依赖
RUN apt-get update && apt-get install --no-install-recommends -y \
    curl \
    build-essential

# 安装 poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# 设置工作目录
WORKDIR $PYSETUP_PATH

# 复制依赖文件并安装依赖
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev --no-interaction --no-ansi

# 生产阶段
FROM python:3.11-slim AS production

# 复用构建阶段的环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv" \
    APP_HOME="/app"

# 将 poetry 和 venv 添加到 PATH
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# 设置工作目录
WORKDIR $APP_HOME

# 从构建阶段复制虚拟环境和应用代码
COPY --from=builder $PYSETUP_PATH $PYSETUP_PATH
COPY ./backend $APP_HOME/backend

# 暴露端口
EXPOSE 80

# 启动命令
CMD ["uvicorn", "api.app.main:app", "--host", "0.0.0.0", "--port", "80"]