# sportSnapshot

Sports data crawled, processed, and visualized

```bash
# first terminal
docker build -t sportsnapshot .
docker run -it sportsnapshot

---> python data/schedule_crawler.py
---> python data/schedule_processor.py

# second terminal
docker container list
docker cp <container_id>:/code/results .
```
