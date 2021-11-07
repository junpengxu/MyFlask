FROM python:3.8

MAINTAINER junpengxu weakeexu@gmail.com

ADD . /code
WORKDIR /code

ARG PORT=8000
RUN /usr/local/bin/python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r /code/requirements.txt --trusted-host pypi.tuna.tsinghua.edu.cn
EXPOSE ${PORT}

CMD ["gunicorn","-w", "2", "-t", "60", "-b", "0.0.0.0:8000", "-k", "gevent", "manage:app"]
