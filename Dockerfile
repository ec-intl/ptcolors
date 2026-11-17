FROM python:3.13-slim-bookworm AS ci-testing
WORKDIR /app
ENV MPLBACKEND=Agg
ENV PYTHONPATH=/app/src:/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt && python -m pip check
COPY . .
CMD ["python", "-m", "pytest", "-v", "--cov", "./src/tests/"]
