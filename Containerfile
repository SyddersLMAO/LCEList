# Running environment
FROM alpine:3.23

# Environment variables
ENV USER_NAME=lcelist
ENV GROUP_NAME=lcelist
ENV UID=1000
ENV GID=1000
ENV HOME_DIR=/home/${USER_NAME}
ENV VIRTUAL_ENV=/app/.venv
ENV PORT=8080

## Install JRE 21
RUN apk add python3 git

## Create Group
RUN addgroup --gid "$GID" "$GROUP_NAME"

## Create User
RUN adduser --uid 1000 -D -S -h ${HOME_DIR} -s /sbin/nologin -G ${GROUP_NAME} ${USER_NAME}

## Set working directory
WORKDIR /app

## Setup a virtual environment
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

## Clone the repository + install depencencies
RUN git clone https://github.com/SyddersLMAO/LCEList/ && cd LCEList && pip install -r requirements.txt

## Change permissions on /app
RUN chown -R ${USER_NAME}:${GROUP_NAME} /app

## Switch user
USER ${USER_NAME}

## Switch to LCEList repo dir
WORKDIR /app/LCEList

## Container setup
CMD python manage.py migrate && python manage.py backfill_loaders && python manage.py collectstatic --noinput && gunicorn lcelist.wsgi --bind 0.0.0.0:$PORT