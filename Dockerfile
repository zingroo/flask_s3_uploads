from alpine:latest

RUN apk add --no-cache python3-dev \
	&&pip3 install --upgrade pip

RUN python3 -m venv venv
RUN chown 777 venv/bin/activate
RUN . venv/bin/activate

WORKDIR /app

COPY /flask_s3_uploads /app

RUN pip3 --no-cache-dir install -r requirements.txt

ENV FLASK_APP app.py


EXPOSE 5000

CMD [ "flask", "run", "--host=0.0.0.0"] 

