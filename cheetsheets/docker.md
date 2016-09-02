# Commands

- Build docker image `docker build -f Dockerfile.elastic -t  <image-name>:latest -t <image-name>:1.0 .`
- Run docker container from image `docker run --detach --restart=always --publish=32775:9200 --name=<container-name> <image-name>`
- Bash into running container `docker exec -it <container-name> /bin/bash`

# Dockerfile

```docker
FROM elasticsearch:latest

# install plugins
# https://github.com/lmenezes/elasticsearch-kopf
# https://www.elastic.co/guide/en/elasticsearch/plugins/current/analysis-icu.html
RUN /usr/share/elasticsearch/bin/plugin install lmenezes/elasticsearch-kopf/2.0 \
    && /usr/share/elasticsearch/bin/plugin install analysis-icu

ADD local/path/to/file/with/script.groovy /usr/share/elasticsearch/config/scripts/script.groovy
```
