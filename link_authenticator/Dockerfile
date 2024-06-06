FROM python

WORKDIR /opt/demo/

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5050

ENTRYPOINT python auth_app.py