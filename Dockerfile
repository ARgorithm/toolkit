FROM alanjohn/argorithm-server:latest

RUN mkdir /package
COPY . /package

# Setup current iteration of ARgorithm
WORKDIR /package
RUN pip install setuptools wheel && \
	python setup.py install && \
    pip install -e .

WORKDIR /app