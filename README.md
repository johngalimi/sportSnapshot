# sportSnapshot

Sports data crawled, processed, and visualized

```bash
# first terminal (db instance)
docker run --name postgres-docker -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres

# second terminal (execute crawling and processing)
docker build -t sportsnapshot .
docker run -it sportsnapshot

---> python data/schedule_crawler.py && python data/schedule_processor.py

# optional terminal (if you want to copy raw crawl results to host)
docker container list
docker cp <container_id>:/code/results .

# server
docker build -f service.Dockerfile . -t sportsservice
docker run --rm -p 5000:5000 sportsservice

# user interface
docker build -f ui.Dockerfile .\src\ui\ -t sportsui
docker kill $(docker ps -q --filter ancestor=sportsui); docker run --rm -p 3000:3000 sportsui
```
