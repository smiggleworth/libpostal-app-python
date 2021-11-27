FROM python:3-alpine AS build

RUN apk update && \
    apk upgrade && \
    apk add --no-cache --virtual .build-deps curl gcc g++ autoconf automake libtool pkgconfig alpine-sdk git bash git openssh && \
    rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/openvenues/libpostal /libpostal

WORKDIR /libpostal
RUN ./bootstrap.sh && \
    ./configure --prefix=/usr --datadir=/usr/share/libpostal && \
    make && \
    make install

FROM python:3-alpine

RUN apk update && \
    apk upgrade && \
    apk add --no-cache build-base

COPY --from=build /usr/share/libpostal /usr/share/libpostal
COPY --from=build /usr/lib/libpostal.so /usr/lib/libpostal.so
COPY --from=build /usr/lib/libpostal.so.1 /usr/lib/libpostal.so.1
COPY --from=build /usr/include/libpostal /usr/include/libpostal

# Copy the requirments.txt
COPY ./requirements.txt ./requirements.txt 

# Fetch app specific dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy our application code
COPY ./app ./app

# Expose port
EXPOSE 80

# Start the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]