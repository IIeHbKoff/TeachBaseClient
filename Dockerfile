FROM python:3.9
RUN apt-get update && apt-get install -y --no-install-recommends gcc htop iputils-ping vim net-tools telnet nmap redis
WORKDIR .
COPY . .
RUN pip install poetry && poetry install
CMD ["/bin/bash", "start.sh"]