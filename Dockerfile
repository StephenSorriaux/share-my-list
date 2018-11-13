FROM python:3.6-alpine3.8

ENV DEBUG=False \
    ADMIN_USERNAME="" \
    ADMIN_EMAIL="" \
    ADMIN_PASSWORD="" \
    ALLOWED_HOSTS=""

VOLUME [ "/usr/app/db" ]
EXPOSE 8000

WORKDIR /usr/app
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY lists ./lists
COPY xmas_list ./xmas_list
COPY manage.py ./manage.py
COPY launch.sh ./launch.sh

ENTRYPOINT [ "/bin/sh", "launch.sh" ]
CMD [ "0.0.0.0:8000" ]