# sportSnapshot

```bash
# first terminal
docker build -t sportsnapshot .
docker run -it sportsnapshot

---> python schedule_crawler.py
---> python schedule_processor.py

# second terminal
docker container list
docker cp ed47aa1fb1b9:/code/results .
```

Sports data crawled, processed, and visualized

Python (BeautifulSoup, Flask), JavaScript (React)
