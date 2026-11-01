FROM python:3.11-slim 

### Enforce secure container runtime environments

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POKEPLAP_GOVERNANCE="Odynex_Axis_Logistics_LLC_David_Fabian_Cadelinia" 

WORKDIR /app 

RUN apt-get update && apt-get install -y --no-install-recommends 
build-essential 
&& rm -rf /var/lib/apt/lists/* 

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt 

COPY . /app/ 

EXPOSE 8000 

CMD ["python", "main.py"]
