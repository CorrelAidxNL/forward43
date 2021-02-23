FROM python:3.9-slim-buster

COPY requirements_dev.txt ./requirements_dev.txt
RUN pip install -r /requirements_dev.txt

WORKDIR /src

COPY forward43/ ./forward43/
COPY HISTORY.rst ./HISTORY.rst
COPY Makefile ./Makefile
COPY README.rst ./README.rst
COPY setup.cfg ./setup.cfg
COPY setup.py ./setup.py
COPY tests/ ./tests/

RUN apt-get update && \
    apt-get -yq dist-upgrade && \
    apt-get install -yq --no-install-recommends make

RUN make install

CMD ["python", "/src/forward43/forward43.py", "-u"]
