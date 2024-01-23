FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

COPY requirements.txt .

ENV TZ=Africa/Johannesburg
RUN ln -snf /usr/share/zoneinfo/$CONTAINER_TIMEZONE /etc/localtime && echo $CONTAINER_TIMEZONE > /etc/timezone


RUN  apt-get update \
  && apt-get install -y wget \
  && rm -rf /var/lib/apt/lists/*

RUN apt-get update

RUN apt-get update && apt-get install -y tzdata && apt-get install -y --no-install-recommends \
  build-essential \
  python3 \
  python3-pip \
  && rm -rf /var/lib/apt/lists/* \
  && pip3 install --no-cache-dir -r requirements.txt

RUN  rm -vf /var/lib/apt/lists/*
RUN apt-get update

 
COPY . .

RUN mkdir -p ~/.streamlit/
RUN echo "[general]"  > ~/.streamlit/credentials.toml
RUN echo "email = \"\""  >> ~/.streamlit/credentials.toml

RUN mkdir -p ~/.streamlit/
RUN echo "\
  [server]\n\
  headless = true\n\
  port = 8501\n\
  enableCORS = false\n\
  \n\
  [theme]\n\
  base = \"light\"\n\
  " > ~/.streamlit/config.toml

RUN echo '[general]\nemail = "a@a.a"' > /root/.streamlit/credentials.toml
RUN echo '[server]\nheadless = true\nenableCORS=false\nport = 8501' > /root/.streamlit/config.toml

RUN apt-get update
  
ENV STREAMLIT_THEME=light


EXPOSE 8501
ENV DISPLAY=:99

CMD streamlit run --server.port 8501 JSE.py