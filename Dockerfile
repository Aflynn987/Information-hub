FROM python:3.6-alpine
MAINTAINER Aaron Flynn
EXPOSE 8000
RUN apk add --no-cache gcc python3-dev musl-dev
ADD . /info-hub
WORKDIR /info-hub
RUN pip install -r requirements.txt
RUN python Information-hub/manage.py makemigrations
RUN python Information-hub/manage.py migrate
CMD [ "python", "Information-hub/manage.py", "runserver", "0.0.0.0:8000" ]