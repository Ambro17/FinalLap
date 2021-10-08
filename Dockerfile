FROM python:3.10.0-slim

# Flags to print immediately and avoid writing .pyc files
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy files and folders into /app
COPY . /app
WORKDIR /app

# Open shell with all required files
# python example.py
# python solution/domain.py
# python solution/main.py
CMD ["/bin/bash"]