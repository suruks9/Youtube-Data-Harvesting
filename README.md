# YouTube Data Harvesting and Warehousing using SQL, MongoDB, and Streamlit

An end-to-end project that demonstrates how to harvest, store, and visualize YouTube data using SQL, MongoDB, and Streamlit.

## Table of Contents

- [Features](#features)
- [Data Configuration](#data-configuration)
- [Usage](#usage)
- [Technologies](#technologies)

## Features

- Harvests YouTube video metadata including title, views, likes, comments, etc.
- Stores harvested data in structured SQL database and unstructured MongoDB collections.
- Provides an interactive web app built with Streamlit for data exploration and visualization.
- Offers multiple chart types such as scatter plots, bar charts, and line charts for insights.
- Supports querying data based on various criteria like video views, likes, and comment counts.

## Data Configuration

## Sample database configuration

- sql:
  host: localhost
  user: your_username
  password: your_password
  database: youtube_data

- mongodb:
   host: localhost
   port: 27017
   username: your_username
   password: your_password
   database: youtube_data

## Usages
 Ensure that data has been harvested and stored in the databases.

Run the Streamlit app to visualize the data:

- Copy code
- 
"streamlit run Youtube Data Harvesting using mongoDb and mysql.py"

Access the app through the provided URL and explore the interactive visualizations.

## Technologies

- Python 3.8+: Data harvesting and processing.
- SQL (MySQL): Structured storage of YouTube data.
- MongoDB: Unstructured storage of YouTube data.
- Streamlit: Interactive data visualization and analysis.
