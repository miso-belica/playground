# Commands

- Build docker image `docker build --rm=true -f Dockerfile --tag <image-name>:latest -t <image-name>:1.0 .`
- Run in foreground `docker run -it --rm --init --publish 80:80 -p 8080:8080 -e "ENV=value" <image-name>`
- Run command `docker run -it --rm --init --publish 80:80 -p 8080:8080 -e "ENV=value" --name=<container-name> <image-name> npm run test`
- Run in background `docker run --detach --restart=always --publish=32775:9200 --name=<container-name> [-v <local-absolute-path>:<docker-absolute-path>] <image-name>`
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
