FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

WORKDIR /app

COPY requirements.txt .

# Install torch CPU-only FIRST, from PyTorch's dedicated CPU index —
# this avoids pulling the much larger CUDA-enabled build by default.
RUN uv pip install --system --no-cache torch --index-url https://download.pytorch.org/whl/cpu

RUN uv pip install --system --no-cache -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]