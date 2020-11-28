# sportSnapshot

Sports data crawled, processed, and visualized

```bash
# first terminal (execute crawling and processing)
docker build -t sportsnapshot .
docker run -it sportsnapshot

---> python data/schedule_crawler.py
---> python data/schedule_processor.py

# second terminal (copy crawl result to host)
docker container list
docker cp <container_id>:/code/results .

# third terminal (db instance)
docker ps -a
docker system prune
docker run --name postgres-docker -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres
```
