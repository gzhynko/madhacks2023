# Where To Go
![where to go logo](./docs/images/logo.png)

Are you a student at UW-Madison? Find out where stuff is happening today using www.wheretogo.tech!!!

## Inspiration
We did not like the [today.wisc.edu](today.wisc.edu) page and wanted to easy see what events were happening on campus on a map to improve the quality of life of students looking for things to do.

## What it does
Displays the events calendar of the [today.wisc.edu](today.wisc.edu) page on an interactive map so that users can find a building with things happening and see what events are there.

## How we built it
We used python for web scraping [today.wisc.edu](today.wisc.edu) for the whole week beginning from the date the site was used and constructed event classes to hold the name, times, date, location, and description. We used MongoDB Atlas to store the great amount of data we scraped from today.wisc.edu. We used Google Cloud functions to scraping the events and then accessing the scraped events from the front-end. We also used the Google Cloud scheduler to run the scraper once a day. 

## Challenges we ran into
While learning web scraping html code, we struggled with the various cases of formatting and a.m., p.m. standardizing as well as locating certain variables. There was also a challenge in learning Google Cloud, how to use the functions and the scheduler. Although we did not have experience with MongoDB Atlas prior, the process was quite smooth.

## Accomplishments that we're proud of
We're are proud of the progress we have made as well as the teamwork we used throughout the 24hrs we have been doing the project and what we have learned.

## What we learned
Web scraping while checking for null and edge cases, Google Cloud with its functions and scheduler, and utilizing databases like MongoDB Atlas. 

## What's next for Where To Go
Adding events in the Madison area and not solely UW-Madison events.

We enjoyed using GitHub as our group members contributed different things and needed others to push their work so that the final product could be great. MongoDB Atlas was a fantastic resource to store the large amount of data we needed to store and it was easy to learn. Google Cloud was very useful as its functions were straightforward to learn and the scheduler is very useful for the data we need to scrape.
