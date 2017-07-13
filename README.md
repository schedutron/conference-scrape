# conference-scrape
Scraping list of open source conferences all over the world.

For a quick demo, do:
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
