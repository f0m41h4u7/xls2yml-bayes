FROM python:3.8.1-alpine3.11

COPY	. /bayes 
WORKDIR	/bayes

ENV PACKAGES="\
	dumb-init \
	musl \
	libc6-compat \
	linux-headers \
	build-base \
	bash \
	git \
	freetype \
	libgfortran \
	libgcc \
	libstdc++ \
	openblas \
	tcl \
	tk \
"

RUN	apk update && apk upgrade 
RUN	apk add --virtual build-runtime \
	build-base python-dev openblas-dev freetype-dev pkgconfig gfortran \
	&& ln -s /usr/include/locale.h /usr/include/xlocale.h \
	&& pip3 install --upgrade pip \
	&& pip3 install --no-cache-dir -r requirements.txt \
	&& apk del build-runtime \
	&& apk add --no-cache --virtual build-dependencies $PACKAGES \
	&& rm -rf /var/cache/apk/*
