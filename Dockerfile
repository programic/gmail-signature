FROM python:3.9-alpine

RUN pip --no-cache-dir install google-api-python-client google-auth-httplib2 google-auth-oauthlib

CMD ["python", "-"]