FROM postgres:alpine3.19
RUN rm -rf /var/lib/postgresql/data
COPY ./init.sql /docker-entrypoint-initdb.d/
