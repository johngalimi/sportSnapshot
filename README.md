# sportSnapshot

Sports data crawled, processed, and visualized

```bash
# first terminal
docker build -t sportsnapshot .
docker run -it sportsnapshot

---> python schedule_crawler.py
---> python schedule_processor.py

# second terminal
docker container list
docker cp <container_id>:/code/results .
```
