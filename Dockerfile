#uses Python 3.12 base image
FROM python:3.12-slim

#inside the container, use /app as the working directory 
WORKDIR /app 

#. means copy re...txt from your computer into /app inside the image
COPY requirements.txt . 

#while builidng the image, install all Python Dependencies listed 
#install CPU-only PyTorch (explicitly controls which Torch build we want)
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu

#add what Docker needs to talk to PostgreSQL, didn't need that inmy pc vecause PostgreSQL client library is available thru the locl setup
RUN apt-get update && apt-get install -y libpq5
RUN pip install -r requirements.txt

#copies the rest of your current project into /app inside the image, first . = everything in your current proj dir to second . = the current /app workdir inside the image
COPY . .

#when a containers start this image, run "python flask_main.py"
CMD ["python", "flask_main.py"] 

# Build Docker image (reuse cached layers when possible) = docker build -t ai-codebase-backend .
# Build Docker image from scratch (ignore cached layers) = docker build --no-cache -t ai-codebase-backend .


# Run a container from Docker Image (running instance of my project) = docker run --rm -p 5001:5001 --env-file .env ai-codebase-backend:latest