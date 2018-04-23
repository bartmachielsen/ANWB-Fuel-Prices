FROM python:3.6
ADD . /app
WORKDIR /app
RUN python -m pip install -r requirements.txt
CMD [ "python", "main.py" ]