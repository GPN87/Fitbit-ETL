# Fitbit ETL (In progress)

![ETL Flow](img/Screen%20Shot%202023-08-07%20at%2010.14.15%20pm.png)

An ETL pipeline that collects and stores batch-processed activity data from my Fitbit into a structured database. 

```Fitbit_requester.py``` automates a daily retrieval of ```steps```, ```heartrate``` and ```runs``` data using the Fitbit API. The extracted data is processed and organized using SQLAlchemy and stored in an SQLite database. 

It was a fun little side project I started in April. The hardest part was actually scheduling the API call. Initially I tried using a cron job but ran into problems with the db schema. Instead, I've used the ```schedule``` library to run the script.

I have the E, T and most of the L done.. now I want to build a dashboard that updates in real time - either in Power BI or with javascript served on Flask.