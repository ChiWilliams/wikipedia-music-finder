FROM python:3.12.3
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY . .

# Make sure the app is accessible from outside
ENV HOST=0.0.0.0