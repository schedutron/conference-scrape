# conference-scrape
Scraping list of open source conferences all over the world.

For a quick demo, do:
```
scrapy crawl papercall -o info.json
```
In place of `papercall`, `oreilly` can also be used.
(Currently only scraping from [papercall.io](http://papercall.io) and [oreilly.com/conferences/](https://www.oreilly.com/conferences/)has been implemented with Scrapy.)

This will create a info.json file in your working directory. Here's a sample of it's contents:
```
[
{"title": "Pro Event: dev up Conference 2017", "description": "Offers travel assistance; Our primary audience is the developer community and the ecosystem around developers. If you have ...", "location": "St. Louis, MO", "time": "Closes July 31, 2017 23:00 UTC", "tags": null, "link": "http://www.devupconf.org", "source": "https://www.papercall.io"},
{"title": "Pro Event: GraphConnect New York", "description": "Share Your Impact Story\r\n\r\n\r\n* **Impact on Innovation**: Where are graphs and Neo4j making a di...", "location": "New York City", "time": "Closes August 01, 2017 07:00 UTC", "tags": ["Impact on technology", "Impact on business", "Deeply technical", "Best practices", "Neo4j for good", "Scaling neo4j", "Data journalism", "Neo4j in the cloud", "Neo4j partner", "Community and open source", "Customer story", "Impact on innovation", "Graph analytics/compute"], "link": "http://graphconnect.com", "source": "https://www.papercall.io"},
{"title": "Pro Event: DNN Summit 2018", "description": "Offers travel assistance; DNN Summit is looking for session submissions on a wide variety of topics.  Our event supports tw...", "location": "Denver, CO", "time": "Closes August 15, 2017 23:00 UTC", "tags": [".net-core", "Client-side", "Performance", "Seo", "Security", "Marketing", "Administration", "Dnn"], "link": "http://www.dnnsummit.org", "source": "https://www.papercall.io"},
{"title": "Pro Event: PyCascades 2018", "description": "Offers travel assistance; Encourage people you know to submit - especially those who wouldn\u2019t normally do so and/or might n...", "location": "Vancouver, BC", "time": "Closes August 29, 2017 12:00 UTC", "tags": null, "link": "http://www.pycascades.com", "source": "https://www.papercall.io"},
{"title": "Pro Event: JVMCON", "description": "Offers travel assistance; We are looking for two types of sessions\r\n\r\n### Talk (60 minutes)\r\n- Should have a clear relat...", "location": "Cinemec, Ede, The Netherlands", "time": "Closes October 17, 2017 23:00 UTC", "tags": null, "link": "http://www.jvmcon.com", "source": "https://www.papercall.io"},
{"title": "GothamGo Go Language Conference", "description": "Offers travel assistance; Share your experience! Submit your presentation proposal to GothamGo, New York City's Go language...", "location": "New York City, Oct 5-6 2017", "time": "Closes July 28, 2017 03:59 UTC", "tags": ["Go", "Golang"], "link": "http://gothamgo.com", "source": "https://www.papercall.io"},
{"title": "DevOpsDays Nashville 2017", "description": "There are three ways to propose a session:\r\n\r\n1.  ***A proposal for a talk/panel*** during the co...", "location": "Nashville, Tennessee", "time": "Closes July 28, 2017 23:00 UTC", "tags": null, "link": "https://www.devopsdays.org/events/2017-nashville/", "source": "https://www.papercall.io"},
]
```
You can scrape without scrapy as well:
```
import scrape_conf
total = scrape_conf.from_paper_call()
```

`from_oreilly()`, `from_opensource()`, `from_pycon_calender()`, `from_lanyrd()` and `from_linuxfoundation()` can also be used.


For pretty output, do:
```
import json
print(json.dumps(total, indent=4))
```
Sample output:
```
[
    {
        "title": "Bristol JS",
        "description": "Offers travel assistance; We're always on the hunt for quality speakers. Since we run monthly talks we will be notifying sp...",
        "location": "Bristol, UK",
        "time": "Closes June 01, 2020 00:00 UTC",
        "tags": [
            "Beginner",
            "Intermediate",
            "Advanced"
        ],
        "link": null,
        "source": "https://www.papercall.io"
    },
    {
        "title": "Ruby Novi Sad Meetup",
        "description": "Napi\u0161ite nekoliko re\u010denica o tome \u0161ta planirate da ispri\u010date i \u0161ta slu\u0161aoci mogu da o\u010dekuju da \u0107e...",
        "location": "Novi Sad, Serbia",
        "time": "Closes November 04, 2020 17:55 UTC",
        "tags": [
            "Ruby",
            "Ecosystem",
            "Rails"
        ],
        "link": "https://www.meetup.com/Ruby-Novi-Sad/",
        "source": "https://www.papercall.io"
    },
    {
        "title": "Docker Novi Sad Meetup",
        "description": "Napi\u0161ite nekoliko re\u010denica o tome \u0161ta planirate da ispri\u010date i \u0161ta slu\u0161aoci mogu da o\u010dekuju da \u0107e...",
        "location": "Novi Sad, Serbia",
        "time": "Closes April 18, 2021 14:44 UTC",
        "tags": [
            "Meetup",
            "Docker",
            "Devops"
        ],
        "link": "https://www.meetup.com/Docker-Novi-Sad/",
        "source": "https://www.papercall.io"
    },
    {
        "title": "CLE.py",
        "description": null,
        "location": null,
        "time": "Closes July 23, 2021 10:23 UTC",
        "tags": [
            "Web techonology",
            "Testing",
            "Advanced",
            "Security",
            "Intermediate",
            "Data science/analysis",
            "Packaging",
            "Python",
            "Beginner",
            "Data processing technology"
        ],
        "link": null,
        "source": "https://www.papercall.io"
    }
]
```
