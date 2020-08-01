FROM python:3.7

WORKDIR /app

COPY gpt2_service.py /app
ADD models /app/models

RUN pip install --no-cache-dir tensorflow-gpu=='1.15.0'
RUN pip install --no-cache-dir uvicorn
RUN pip install --no-cache-dir fastapi
RUN pip install --no-cache-dir gpt-2-simple

CMD [ "python3", "gpt2_service.py" ]
