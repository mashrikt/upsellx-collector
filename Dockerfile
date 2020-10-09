FROM nikolaik/python-nodejs:latest
WORKDIR /app
ENV PYTHONUNBUFFERED=1
ADD . /app/
RUN npm install -g serverless && npm install
RUN pip install --upgrade pip && pip install -r requirements.txt
