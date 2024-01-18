# WARNING - if you change this file you need to update the pes-kafka-connect Dockerfile with a new base image
FROM Redacted.dkr.ecr.us-east-1.amazonaws.com/mirror/docker.io/debian:bullseye-20240110-slim AS jre-build

RUN sed -i 's/http/https/g' /etc/apt/sources.list
RUN echo 'Acquire::https::Verify-Peer "false";' >/etc/apt/apt.conf.d/80-ignore-tls
RUN apt-get update && apt-get install -y ca-certificates && rm -f /etc/apt/apt.conf.d/80-ignore-tls
RUN apt-get install -y wget apt-transport-https gnupg software-properties-common
RUN wget -O- https://apt.corretto.aws/corretto.key | apt-key add -
RUN add-apt-repository 'deb https://apt.corretto.aws stable main'
# Keep in sync with JDK_VERSION
RUN apt-get update && apt-get install -y java-17-amazon-corretto-jdk=1:17.0.10.7-1
RUN apt-get upgrade -y
RUN apt-get install -y gettext jq supervisor
RUN addgroup --system test && adduser --uid 1101 --system test --ingroup test --home /test
RUN mkdir /test/data /test/plugins /test/ssl

# Keep in sync with KAFKA_VERSION KAFKA_CONNECT
RUN wget https://archive.apache.org/dist/kafka/3.4.0/kafka_2.13-3.4.0.tgz -O - | tar -xz -C / && mv kafka_2.13-3.4.0 kafka
# Keep in sync with AWS_MSK_IAM_AUTH
RUN wget https://github.com/aws/aws-msk-iam-auth/releases/download/v2.0.2/aws-msk-iam-auth-2.0.2-all.jar -P /kafka/libs/
RUN cp `dirname $(dirname $(readlink -f $(which java)))`/lib/security/cacerts /test/ssl/truststore.jks && chmod 644 /test/ssl/truststore.jks

ENV PATH=$PATH:/kafka/bin:/test/bin KAFKA_CONNECT_REST_API_PORT=8083

COPY docker/test test

RUN chown -R test:test /test /kafka
USER test
WORKDIR /test
