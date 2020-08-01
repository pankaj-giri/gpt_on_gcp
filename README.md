# Deploying gpt2 on Google Cloud Platform
A step by step approach to deploying GPT2 based service on GCP as a docker container

# Dependencies
fastapi
tensorflow==1.15.0
gpt-2-simple==0.7.1

# Steps

The python runtime with the service is packaged into a docker image and pushed into Google Cloud registry and finally deployed.

This file ```gpt2_service.py``` exposes gpt2 as a Fastapi rest service

The Python 3 Dockerfile starts a Fastapi web server that listens on the port 8080:

```
FROM python:3.7

WORKDIR /app

COPY gpt2_service.py /app
ADD models /app/models

RUN pip install --no-cache-dir tensorflow-gpu=='1.15.0'
RUN pip install --no-cache-dir uvicorn
RUN pip install --no-cache-dir fastapi
RUN pip install --no-cache-dir gpt-2-simple

CMD [ "python3", "gpt2_service.py" ]
```

Build your container image using Cloud Build, by running the following command from the directory containing the Dockerfile:

```
gcloud builds submit --tag gcr.io/<PROJECT_ID>/<docker-REPO:TAG>
```
Eg.

```
gcloud builds submit --tag gcr.io/cobalt-baton-282213/nlg:gpt2_service
```
where PROJECT-ID is your GCP project ID. You can get it by running 
<br>```gcloud config get-value project```

To deploy this please run
```
gcloud run deploy --image gcr.io/cobalt-baton-282213/nlg:gpt2_service --platform managed --memory 2048M
```

To access this service please check 

https://nlg-tkclnkiika-de.a.run.app/docs

This opens up a Swagger UI, and you could have a go at the service, by clicking ```get``` on  ```​/predict​/{prefix}``` api.
Then click ```Try it out```, and then write something on the ```prefix``` text box and click execute.



# References
https://cloud.google.com/run/docs/quickstarts/build-and-deploy#python