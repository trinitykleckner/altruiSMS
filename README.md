# AltruiSMS 

## Elevator Pitch
We present Phil, an SMS chat bot to notify the homeless and hungry of shelters and welfare distribution anywhere, at any time.

## See demo [here](https://youtu.be/Za9T4aq0ilw)

## Inspiration
In Philadelphia, many homeless and hungry people do not have stable internet access. Hence, it is difficult for them to reliably communicate with them about where the distribution of food and daily necessities are taking place. Hence, we want to create a SMS chat bot that connects the homeless and hungry with voluntary welfare organizations and churches.


## What it does
In a world where event communication is almost entirely online, we cannot omit those without stable internet, especially when it comes to events distributing the resources they need most. Our SMS welfare-distribution notification system provides those who need it with not just alerts, but an SMS chat bot that is ready to assist them at any time!

Through a conversation with Phil, our SMS chat bot, users can opt into receiving text notifications when local organizations are holding distribution events for items of their choosing (food, diapers, sanitary products, etc.). Organizations can register on our application to post upcoming events they are holding. They can also see when and where other organizations are distributing supplies to better coordinate efforts for effective distribution of daily necessities throughout the year. When registering, organizations are strongly encouraged to note if they are a 24-hour shelter. This information allows our chatbot feature to find the nearest shelter for anyone at any time. In accordance with our goal of making this chatbot as accessible and inclusive as possible, we ask for no personal information; we only communicate based on mobile messaging and request for the user’s items of interest, and the user’s location via a nearby street intersection. User information can be easily updated or deleted to protect the user’s privacy.


## How we built it
We centered our application around Django’s backend framework by tapping on the extensive API and object relation model libraries. To connect our users to the database, we set up a Twilio trial account and obtained a phone number that now serves as the number for our SMS chat bot. We connected the Twilio phone number to the Django server to process the user’s inputs and return meaningful and helpful responses. We stored the user’s preferences in our SQLite database using Django’s object relation model tools. We connected our Django server to Mapbox API and Translate API to tap on the powerful geocoding, location, and translation services that they offer to better serve our users’ needs.

We built a web application that functions as an interface for organizations to register their organization and create welfare distribution events that would be disseminated to users with relevant preferences. We set up the web application to use Django and Bootstrap for smooth integration with our Django backend and a seamless user experience for the organizations. The web application also has a dashboard that offers data analytics for the organizations that quantify the impact of their outreach activities. 

Lastly, we deployed our application using Heroku to allow our product to provide continued support to our customers. 


## Challenges we ran into
We recognized the importance of subreddits such as r/freebies and r/Freefood have, as they are updated in real-time and conglomerate relevant information on free necessities by users. As part of our initiative to make events more accessible to individuals with limited Wi-Fi access, we tried to web scrape them for posts pertaining to viable businesses in the Philadelphia area. This was executed using PRAW, a Reddit API Wrapper, and generated a CSV file containing the posts score, title, comments, URL link, and timestamp. However, categorizing them into the objects created for altruiSMS proved difficult given the ambiguity of miscellaneous tags accompanying Reddit posts. We attempted NLP to recognize each of the tags however reddit flairs conflicted with those tags, giving incorrect predictions for the posts. This resulted in the events being incorrectly labeled in the wrong object when creating the event in altruiSMS.

Because offers in these subreddits are time-sensitive, and new posts are updated frequently, periodically scraping these subreddits proved vital to its success. This was complicated with the issue of HTTP Function triggers not deploying correctly. Microsoft Azure was first used to create resource groups and run the python scraping, which did not have the ability to share the resulting CSV file in its database publicly in a secure manner. We migrated to Google Cloud Platform in an attempt to run the script with localized access to the database, however, the script used unrecognizable packages and failed to deploy.


## Accomplishments that we're proud of
- Effectively and smoothly integrating the multitude of technologies into one cohesive project. 
- Making Phil bi-lingual, by including both English and Spanish (the second most spoken language in Philly) we were able to further increase the accessibility of AltruiSMS.
- Persevering through the week, especially with a hectic schedule of homework, exams, and papers. 


## What we learned
We learned how to better take advantage of the frameworks and APIs that are available online. Even though we had a clear idea of the functionalities, it was daunting imagining how we ought to build those features. However, we persevered and figured out how to integrate the various APIs and frameworks into a cohesive application that offers our users a variety of useful features. We were also given the opportunity to further hone our software development skills and explore features in Twilio and Django that we have not used before. Last but not least, we were able to practice and learn some of the key design principles i.e. user-driven development when we conceptualized the different features that would benefit our users the most.


## What's next for AltruiSMS
- Automate subreddit integration into the events
- Add further language options for Phil
- Using NLP make Phil a conversational SMS bot rather than operating on key words
- Analysis on the most popular shelters to figure out allocation of funding, etc.
- Work with CodeForPhilly (justify by saying they are well-connected with charity organizations) to see if they can bring other organizations on board and find a group of long-term volunteers to maintain this project	
- Spread awareness of our product
- Expand to other cities
