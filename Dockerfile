FROM registry.cn-hangzhou.aliyuncs.com/miclon/py-nodejs:latest as build
WORKDIR /app
COPY . /app
RUN cd /app/web && pnpm install && pnpm run build

FROM python:3.11-slim
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY start.sh /app
COPY api.py /app
COPY server.py /app
CMD ["/bin/bash", "start.sh"]
