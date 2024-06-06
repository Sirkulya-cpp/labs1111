FROM python

WORKDIR /opt/demo/
COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 5000
CMD [ "flask", "--app" , "link_app", "run", "-h", "0.0.0.0", "-p", "5000"]