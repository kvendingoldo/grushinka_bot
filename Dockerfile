FROM python:3

ENV HOME=/opt/grushinka

RUN mkdir -p ${HOME}

COPY requirements.txt ${HOME}
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r ${HOME}/requirements.txt

COPY ./src ${HOME}/src
COPY ./resources ${HOME}/resources

WORKDIR ${HOME}/src

ENTRYPOINT ["python3", "main.py"]