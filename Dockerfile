FROM public.ecr.aws/lambda/python:3.11

COPY requirements.txt ${LAMBDA_TASK_ROOT}/
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py conjugation.py models.py lambda_handler.py ${LAMBDA_TASK_ROOT}/
COPY languages/ ${LAMBDA_TASK_ROOT}/languages/

CMD ["lambda_handler.handler"]
