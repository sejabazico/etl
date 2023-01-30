FROM python:3.10-slim-bullseye
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "entrypoint_estoque.py"]