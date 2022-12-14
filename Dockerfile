# syntax=docker/dockerfile:1
FROM quay.io/qiime2/core:2022.8

COPY . ./
WORKDIR .
ADD requirements.txt ./
RUN python -m pip install -r requirements.txt