FROM python:3.8-slim-buster

RUN apt-get update && apt-get upgrade -y
RUN apt-get -y install python3-pyqt5
# next 2 are for PyQt5
RUN apt-get -y install libnss3
RUN apt-get -y install libasound2

WORKDIR /app

RUN python3 -m pip install --upgrade pip

# so PyQt5 can work
ENV QT_QPA_PLATFORM=offscreen

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8080

# no-sandbox so PyQt5 can work
CMD ["python3", "main.py", "--no-sandbox"]
