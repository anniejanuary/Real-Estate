# Build from minimal image for speed and security
FROM python:3.10.2-slim-bullseye

ENV WORKDIR=/code
ENV USER=code
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR $WORKDIR

COPY ./requirements.txt $WORKDIR
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Add user without root privileges and set access to workdir - for security reasons
RUN adduser --system --group $USER

COPY ./app $WORKDIR
RUN chown -R $USER:$USER $WORKDIR
USER $USER