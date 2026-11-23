FROM python:3.13-slim

ENV TZ=Asia/Seoul \
    LANG=ko_KR.UTF-8 \
    LANGUAGE=ko_KR:ko \
    LC_ALL=ko_KR.UTF-8 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# 시스템 도구 + Node.js(Claude Code CLI 실행용) + 로케일
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        git \
        procps \
        locales \
        nodejs \
        npm \
    && rm -rf /var/lib/apt/lists/* \
    && sed -i '/ko_KR.UTF-8/s/^# //g' /etc/locale.gen \
    && locale-gen \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone

# Claude Code CLI
RUN npm install -g @anthropic-ai/claude-code \
    && npm cache clean --force

# Antigravity CLI 네이티브 바이너리 설치
RUN curl -fsSL https://antigravity.google/cli/install.sh | bash

# PATH 등록
ENV PATH="/root/.local/bin:${PATH}"

# Python 패키지 (langfuse SDK 등)
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /apps

RUN git clone https://github.com/yojulab/learn_Loop_engineering.git \
    && cp -a /apps/learn_Loop_engineering /opt/learn_Loop_engineering

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

WORKDIR /apps/learn_Loop_engineering

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["sleep", "infinity"]
