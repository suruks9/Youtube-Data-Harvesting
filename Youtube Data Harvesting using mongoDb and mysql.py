import googleapiclient.discovery
from googleapiclient.discovery import build
import json
import re
import pymongo
import mysql.connector
import sqlalchemy
from sqlalchemy import create_engine
# import pymysql
import pandas as pd
import numpy as np
import plotly.express as px
from googleapiclient.errors import HttpError
import streamlit as st
from streamlit_option_menu import option_menu
from googleapiclient.discovery import build
import pymongo

if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.Get_state = None

import streamlit as st

if 'Get_state' not in st.session_state:
    st.session_state['Get_state'] = None

# Now you can access or modify st.session_state.Get_state


# Now you can access or modify attributes in st.session_state


st.set_page_config(layout='wide')

# Set your YouTube API credentials here
API_KEY = "AIzaSyBO-7DH7Ou-gw3zxZuH3MMm5y4CVkNm4rE"

# Create a YouTube API service
youtube = build("youtube", "v3", developerKey=API_KEY)


def main():
    st.title("YouTube Data Harvesting and Warehousing")
    selected = option_menu(
        menu_title=None,
        options=["Project Overview and Objectives", "Data Collection", "Storing Data in MongoDB", "Data Migration to MySQL", "Data Analysis"],
        icons=["pencil-fill", "bar-chart-fill"],
        orientation="horizontal",

        #"UC5p2HB41JVstSICaaqOr_oA", "UCCya-YUszMuiTAR3lfYMuog", "UCBnnsrvmuQ7tFdTL511dzBQ", "UC4950gpY6Qw1lCAcN6gNWwQ"

    )
    data = {
        "Channel Name": ["GADGETS ONE MALAYALAM TECH TIPS ","Mr Perfect Tech","Malayalam Tech - മലയാളം ടെക്",
                       "Ebadu Rahman Tech","Tech Catcher","PrathapGTech","Sarath'S Neon Tech","Malayalam Tech Factory","Alex 4 Tech",
                       "Tech 4 Malayalam"],
        "Channel ID": ["UC5p2HB41JVstSICaaqOr_oA", "UCCya-YUszMuiTAR3lfYMuog", "UCBnnsrvmuQ7tFdTL511dzBQ", "UC4950gpY6Qw1lCAcN6gNWwQ",
                         "UCEqxMIEiUNl7xhlY5l32Iyg", "UCn4S6ONdetkpxfuOteHVHhQ", "UCHLmaPy_UYFvQcUp-FdpxRg","UCr0ghRVQoUzlr1i_-DwFJiQ",
                         "UC7dz4uVtNi27lBKVHKv3T9w","UCJPYTDq_fsywsegZpdCjuxQ",]

    }

    if selected =="Project Overview and Objectives":
        st.markdown("## Project Overview")
        st.write("The YouTube Data Harvesting project involves collecting, storing, and analyzing data from YouTube channels and videos. The project utilizes the YouTube Data API to fetch information about channels, videos, comments, and related data. The collected data is then stored in both MongoDB and MySQL databases for further analysis and visualization.")

        st.write("MongoDB is used to store the raw and structured data from YouTube. It's a NoSQL database that allows for flexible and schema-less data storage. In this project, MongoDB stores details about channels, videos, and comments, including information like channel name, subscriber count, video views, video descriptions, comment texts, and more. The flexibility of MongoDB is particularly useful when dealing with varying data structures and nested documents, as found in YouTube's API responses.")

        st.write("MySQL, on the other hand, is a relational database system. It's used to structure and organize the collected data for efficient querying and analysis. The project involves migrating data from MongoDB to MySQL, transforming and shaping it into tables with proper relationships. MySQL's structured nature makes it suitable for running complex queries, aggregations, and analytics on the collected data.")

        st.subheader("The project is likely to involve several stages:")

        st.write("1. Data Collection: Using the YouTube Data API, the project gathers channel details, video information, and comments. The collected data includes metadata like titles, descriptions, view counts, likes, and more.")

        st.write("2. Data Storage in MongoDB: The raw data collected from the API responses is stored in MongoDB. Due to its flexible schema, MongoDB can accommodate the varying data structures from different API calls.")

        st.write("3. Data Transformation: The data collected in MongoDB is transformed and structured into more traditional table structures suitable for MySQL. This includes creating relationships between channels, playlists, videos, and comments.")

        st.write("4. Data Migration: The transformed data is then migrated from MongoDB to MySQL. The data is inserted into the corresponding tables with appropriate data types.")

        st.write("5. Data Analysis: Using SQL queries and analytics tools, you can perform various analyses on the collected data. This could involve querying for top videos, popular channels, user engagement, and more.")

        st.write("6. and graphs to visualize the insights obtained from the data analysis.")

        st.subheader("Summary")

        st.write("In summary, the YouTube data harvesting project combines the strengths of both MongoDB and MySQL: MongoDB's flexibility for initial data storage and handling dynamic structures, and MySQL's structured nature for efficient querying and complex analysis. The end result is a powerful system that allows you to extract valuable insights from YouTube data for research, business decisions, or personal interests.")


    # Create a pandas DataFrame
    df = pd.DataFrame(data)
    if selected == "Data Collection":
        st.subheader("Channel Name and ID Collection")
        st.dataframe(df)


    if selected == "Storing Data in MongoDB":

        col1, col2 = st.columns(2)
        with col1:
            st.header('Data collection')
            channel_id = st.text_input('Enter 11 digit channel_id')
            Get_data = st.button('Store in MongoDB')

            # Define Session state to Get data button
            if "Get_state" not in st.session_state:
                st.session_state.Get_state = False
            if Get_data or st.session_state.get("Get_state", False):
                st.session_state.Get_state = True

                # Define a function to retrieve channel data
                def get_channel_data(youtube, channel_id):
                    try:
                        try:
                            channel_request = youtube.channels().list(
                                part='snippet,statistics,contentDetails',
                                id=channel_id)
                            channel_response = channel_request.execute()

                            if 'items' not in channel_response:
                                st.write(f"Invalid channel id: {channel_id}")
                                st.error("Enter the correct 11-digit **channel_id**")
                                return None

                            return channel_response

                        except HttpError as e:
                            st.error(
                                'Server error (or) Check your internet connection (or) Please Try again after a few minutes',
                                icon='🚨')
                            st.write('An error occurred: %s' % e)
                            return None
                    except:
                        st.write('You have exceeded your YouTube API quota. Please try again tomorrow.')

                # Function call to Get Channel data from a single channel ID
                channel_data = get_channel_data(youtube, channel_id)

                # Process channel data
                # Extract required information from the channel_data
                channel_name = channel_data['items'][0]['snippet']['title']
                channel_video_count = channel_data['items'][0]['statistics']['videoCount']
                channel_subscriber_count = channel_data['items'][0]['statistics']['subscriberCount']
                channel_view_count = channel_data['items'][0]['statistics']['viewCount']
                channel_description = channel_data['items'][0]['snippet']['description']
                channel_playlist_id = channel_data['items'][0]['contentDetails']['relatedPlaylists']['uploads']

                # Format channel_data into dictionary
                channel = {
                    "Channel_Details": {
                        "Channel_Name": channel_name,
                        "Channel_Id": channel_id,
                        "Video_Count": channel_video_count,
                        "Subscriber_Count": channel_subscriber_count,
                        "Channel_Views": channel_view_count,
                        "Channel_Description": channel_description,
                        "Playlist_Id": channel_playlist_id
                    }
                }

                # Define a function to retrieve video IDs from channel playlist
                def get_video_ids(youtube, channel_playlist_id):

                    video_id = []
                    next_page_token = None
                    while True:
                        # Get playlist items
                        request = youtube.playlistItems().list(
                            part='contentDetails',
                            playlistId=channel_playlist_id,
                            maxResults=50,
                            pageToken=next_page_token)
                        response = request.execute()

                        # Get video IDs
                        for item in response['items']:
                            video_id.append(item['contentDetails']['videoId'])

                        # Check if there are more pages
                        next_page_token = response.get('nextPageToken')
                        if not next_page_token:
                            break

                    return video_id

                # Function call to Get  video_ids using channel playlist Id
                video_ids = get_video_ids(youtube, channel_playlist_id)

                # Define a function to retrieve video data
                def get_video_data(youtube, video_ids):

                    video_data = []
                    for video_id in video_ids:
                        try:
                            # Get video details
                            request = youtube.videos().list(
                                part='snippet, statistics, contentDetails',
                                id=video_id)
                            response = request.execute()

                            video = response['items'][0]

                            # Get comments if available (comment function call)
                            try:
                                video['comment_threads'] = get_video_comments(youtube, video_id, max_comments=2)
                            except:
                                video['comment_threads'] = None

                            # Duration format transformation (Duration format transformation function call)
                            duration = video.get('contentDetails', {}).get('duration', 'Not Available')
                            if duration != 'Not Available':
                                duration = convert_duration(duration)
                            video['contentDetails']['duration'] = duration

                            video_data.append(video)

                        except:
                            st.write('You have exceeded your YouTube API quota. Please try again tomorrow.')

                    return video_data

                # Define a function to retrieve video comments
                def get_video_comments(youtube, video_id, max_comments):

                    request = youtube.commentThreads().list(
                        part='snippet',
                        maxResults=max_comments,
                        textFormat="plainText",
                        videoId=video_id)
                    response = request.execute()

                    return response

                # Define a function to convert duration
                def convert_duration(duration):
                    regex = r'PT(\d+H)?(\d+M)?(\d+S)?'
                    match = re.match(regex, duration)
                    if not match:
                        return '00:00:00'
                    hours, minutes, seconds = match.groups()
                    hours = int(hours[:-1]) if hours else 0
                    minutes = int(minutes[:-1]) if minutes else 0
                    seconds = int(seconds[:-1]) if seconds else 0
                    total_seconds = hours * 3600 + minutes * 60 + seconds
                    return '{:02d}:{:02d}:{:02d}'.format(int(total_seconds / 3600), int((total_seconds % 3600) / 60),
                                                         int(total_seconds % 60))

                # Function call to Get Videos data and comment data from video ids
                video_data = get_video_data(youtube, video_ids)

                # video details processing
                videos = {}
                for i, video in enumerate(video_data):
                    video_id = video['id']
                    video_name = video['snippet']['title']
                    video_description = video['snippet']['description']
                    tags = video['snippet'].get('tags', [])
                    published_at = video['snippet']['publishedAt']
                    view_count = video['statistics']['viewCount']
                    like_count = video['statistics'].get('likeCount', 0)
                    dislike_count = video['statistics'].get('dislikeCount', 0)
                    favorite_count = video['statistics'].get('favoriteCount', 0)
                    comment_count = video['statistics'].get('commentCount', 0)
                    duration = video.get('contentDetails', {}).get('duration', 'Not Available')
                    thumbnail = video['snippet']['thumbnails']['high']['url']
                    caption_status = video.get('contentDetails', {}).get('caption', 'Not Available')
                    comments = 'Unavailable'

                    # Handle case where comments are enabled
                    if video['comment_threads'] is not None:
                        comments = {}
                        for index, comment_thread in enumerate(video['comment_threads']['items']):
                            comment = comment_thread['snippet']['topLevelComment']['snippet']
                            comment_id = comment_thread['id']
                            comment_text = comment['textDisplay']
                            comment_author = comment['authorDisplayName']
                            comment_published_at = comment['publishedAt']
                            comments[f"Comment_Id_{index + 1}"] = {
                                'Comment_Id': comment_id,
                                'Comment_Text': comment_text,
                                'Comment_Author': comment_author,
                                'Comment_PublishedAt': comment_published_at
                            }

                    # Format processed video data into dictionary
                    videos[f"Video_Id_{i + 1}"] = {
                        'Video_Id': video_id,
                        'Video_Name': video_name,
                        'Video_Description': video_description,
                        'Tags': tags,
                        'PublishedAt': published_at,
                        'View_Count': view_count,
                        'Like_Count': like_count,
                        'Dislike_Count': dislike_count,
                        'Favorite_Count': favorite_count,
                        'Comment_Count': comment_count,
                        'Duration': duration,
                        'Thumbnail': thumbnail,
                        'Caption_Status': caption_status,
                        'Comments': comments
                    }

                # combine channel data and videos data to a dict
                final_output = {**channel, **videos}

                # create a client instance of MongoDB
                client = pymongo.MongoClient('mongodb://localhost:27017/')

                # create a database or use existing one
                mydb = client['youtube_data']

                # create a collection
                collection = mydb['channel']

                # define the data to insert
                final_output_data = {
                    'Channel_Name': channel_name,
                    "Channel_data": final_output
                }

                # insert or update data in the collection
                upload = collection.replace_one({'_id': channel_id}, final_output_data, upsert=True)

                # print the result of the insertion operation
                st.write(f"Updated document id: {upload.upserted_id if upload.upserted_id else upload.modified_count}")

                # Close the connection
                client.close()

    if selected == "Data Migration to MySQL":

        st.header('Data Shift')

        # Connect to the MongoDB server
        client = pymongo.MongoClient("mongodb://localhost:27017/")

        # create a database or use existing one
        mydb = client['youtube_data']

        # create a collection
        collection = mydb['channel']

        # Collect all document names and give them
        document_names = []
        for document in collection.find():
            document_names.append(document["Channel_Name"])
        document_name = st.selectbox('Select Channel name', options=document_names, key='document_names')
        Migrate = st.button('Migrate to MySQL')

        # Define Session state to Migrate to MySQL button
        if 'migrate_sql' not in st.session_state:
            st.session_state_migrate_sql = False
        if Migrate or st.session_state_migrate_sql:
            st.session_state_migrate_sql = True

            # Retrieve the document with the specified name
            result = collection.find_one({"Channel_Name": document_name})
            client.close()

            # Channel data json to df
            channel_details_to_sql = {
                "Channel_Name": result['Channel_Name'],
                "Channel_Id": result['_id'],
                "Video_Count": result['Channel_data']['Channel_Details']['Video_Count'],
                "Subscriber_Count": result['Channel_data']['Channel_Details']['Subscriber_Count'],
                "Channel_Views": result['Channel_data']['Channel_Details']['Channel_Views'],
                "Channel_Description": result['Channel_data']['Channel_Details']['Channel_Description'],
                "Playlist_Id": result['Channel_data']['Channel_Details']['Playlist_Id']
            }
            channel_df = pd.DataFrame.from_dict(channel_details_to_sql, orient='index').T

            # playlist data json to df
            playlist_tosql = {"Channel_Id": result['_id'],
                              "Playlist_Id": result['Channel_data']['Channel_Details']['Playlist_Id']
                              }
            playlist_df = pd.DataFrame.from_dict(playlist_tosql, orient='index').T

            # video data json to df
            video_details_list = []
            for i in range(1, len(result['Channel_data']) - 1):
                video_details_tosql = {
                    'Playlist_Id': result['Channel_data']['Channel_Details']['Playlist_Id'],
                    'Video_Id': result['Channel_data'][f"Video_Id_{i}"]['Video_Id'],
                    'Video_Name': result['Channel_data'][f"Video_Id_{i}"]['Video_Name'],
                    'Video_Description': result['Channel_data'][f"Video_Id_{i}"]['Video_Description'],
                    'Published_date': result['Channel_data'][f"Video_Id_{i}"]['PublishedAt'],
                    'View_Count': result['Channel_data'][f"Video_Id_{i}"]['View_Count'],
                    'Like_Count': result['Channel_data'][f"Video_Id_{i}"]['Like_Count'],
                    'Dislike_Count': result['Channel_data'][f"Video_Id_{i}"]['Dislike_Count'],
                    'Favorite_Count': result['Channel_data'][f"Video_Id_{i}"]['Favorite_Count'],
                    'Comment_Count': result['Channel_data'][f"Video_Id_{i}"]['Comment_Count'],
                    'Duration': result['Channel_data'][f"Video_Id_{i}"]['Duration'],
                    'Thumbnail': result['Channel_data'][f"Video_Id_{i}"]['Thumbnail'],
                    'Caption_Status': result['Channel_data'][f"Video_Id_{i}"]['Caption_Status']
                }
                video_details_list.append(video_details_tosql)
            video_df = pd.DataFrame(video_details_list)

            # Comment data json to df
            Comment_details_list = []
            for i in range(1, len(result['Channel_data']) - 1):
                comments_access = result['Channel_data'][f"Video_Id_{i}"]['Comments']
                if comments_access == 'Unavailable' or (
                        'Comment_Id_1' not in comments_access or 'Comment_Id_2' not in comments_access):
                    Comment_details_tosql = {
                        'Video_Id': 'Unavailable',
                        'Comment_Id': 'Unavailable',
                        'Comment_Text': 'Unavailable',
                        'Comment_Author': 'Unavailable',
                        'Comment_Published_date': 'Unavailable',
                    }
                    Comment_details_list.append(Comment_details_tosql)

                else:
                    for j in range(1, 3):
                        Comment_details_tosql = {
                            'Video_Id': result['Channel_data'][f"Video_Id_{i}"]['Video_Id'],
                            'Comment_Id':
                                result['Channel_data'][f"Video_Id_{i}"]['Comments'][f"Comment_Id_{j}"][
                                    'Comment_Id'],
                            'Comment_Text':
                                result['Channel_data'][f"Video_Id_{i}"]['Comments'][f"Comment_Id_{j}"][
                                    'Comment_Text'],
                            'Comment_Author':
                                result['Channel_data'][f"Video_Id_{i}"]['Comments'][f"Comment_Id_{j}"][
                                    'Comment_Author'],
                            'Comment_Published_date':
                                result['Channel_data'][f"Video_Id_{i}"]['Comments'][f"Comment_Id_{j}"][
                                    'Comment_PublishedAt'],
                        }
                        Comment_details_list.append(Comment_details_tosql)
            Comments_df = pd.DataFrame(Comment_details_list)

            # Connect to the MySQL server
            connect = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Suruks632",
            )

            # Create a new database and use
            mycursor = connect.cursor()
            mycursor.execute("CREATE DATABASE IF NOT EXISTS youtube_database_1")

            # Close the cursor and database connection
            mycursor.close()
            connect.close()

            # Connect to the new created database
            engine = create_engine('mysql+mysqlconnector://root:Suruks632@localhost:3306/youtube_database_1',
                                   echo=False)

            # Use pandas to insert the DataFrames data to the SQL Database -> table1

            # Channel data to SQL
            channel_df.to_sql('channel', con=engine, if_exists='append', index=False,
                              dtype={"Channel_Name": sqlalchemy.types.VARCHAR(length=225),
                                     "Channel_Id": sqlalchemy.types.VARCHAR(length=225),
                                     "Video_Count": sqlalchemy.types.INT,
                                     "Subscriber_Count": sqlalchemy.types.BigInteger,
                                     "Channel_Views": sqlalchemy.types.BigInteger,
                                     "Channel_Description": sqlalchemy.types.TEXT,
                                     "Playlist_Id": sqlalchemy.types.VARCHAR(length=225), })

            # Playlist data to SQL
            playlist_df.to_sql('playlist', engine, if_exists='append', index=False,
                               dtype={"Channel_Id": sqlalchemy.types.VARCHAR(length=225),
                                      "Playlist_Id": sqlalchemy.types.VARCHAR(length=225), })

            # Video data to SQL
            video_df.to_sql('video', engine, if_exists='append', index=False,
                            dtype={'Playlist_Id': sqlalchemy.types.VARCHAR(length=225),
                                   'Video_Id': sqlalchemy.types.VARCHAR(length=225),
                                   'Video_Name': sqlalchemy.types.VARCHAR(length=225),
                                   'Video_Description': sqlalchemy.types.TEXT,
                                   'Published_date': sqlalchemy.types.String(length=50),
                                   'View_Count': sqlalchemy.types.BigInteger,
                                   'Like_Count': sqlalchemy.types.BigInteger,
                                   'Dislike_Count': sqlalchemy.types.INT,
                                   'Favorite_Count': sqlalchemy.types.INT,
                                   'Comment_Count': sqlalchemy.types.INT,
                                   'Duration': sqlalchemy.types.VARCHAR(length=1024),
                                   'Thumbnail': sqlalchemy.types.VARCHAR(length=225),
                                   'Caption_Status': sqlalchemy.types.VARCHAR(length=225), })

            # Commend data to SQL
            Comments_df.to_sql('comments', engine, if_exists='append', index=False,
                               dtype={'Video_Id': sqlalchemy.types.VARCHAR(length=225),
                                      'Comment_Id': sqlalchemy.types.VARCHAR(length=225),
                                      'Comment_Text': sqlalchemy.types.TEXT,
                                      'Comment_Author': sqlalchemy.types.VARCHAR(length=225),
                                      'Comment_Published_date': sqlalchemy.types.String(length=50), })

    if selected == "Data Analysis":
        # Selectbox creation
        question_tosql = st.selectbox('Select your Question',
                                      ('', '1. What are the names of all the videos and their corresponding channels?',
                                       '2. Which channels have the most number of videos, and how many videos do they have?',
                                       '3. What are the top 10 most viewed videos and their respective channels?',
                                       '4. How many comments were made on each video, and what are their corresponding video names?',
                                       '5. Which videos have the highest number of likes, and what are their corresponding channel names?',
                                       '6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?',
                                       '7. What is the total number of views for each channel, and what are their corresponding channel names?',
                                       '8. What are the names of all the channels that have published videos in the year 2022?',
                                       '9. What is the average duration of all videos in each channel, and what are their corresponding channel names?',
                                       '10. Which videos have the highest number of comments, and what are their corresponding channel names?'),
                                      key='collection_question')

        if question_tosql:
            connect_for_question = mysql.connector.connect(host='localhost', user='root', password='Suruks632',
                                                           db='youtube_database_1')
            cursor = connect_for_question.cursor()

            # data for the plot
            data = px.data.iris()


            # Q1
            if question_tosql == '1. What are the names of all the videos and their corresponding channels?':
                cursor.execute(
                    "SELECT channel.Channel_Name, video.Video_Name FROM channel JOIN playlist JOIN video ON channel.Channel_Id = playlist.Channel_Id AND playlist.Playlist_Id = video.Playlist_Id;")
                result_1 = cursor.fetchall()
                df1 = pd.DataFrame(result_1, columns=['Channel Name', 'Video Name']).reset_index(drop=True)
                df1.index += 1
                st.dataframe(df1)

                # Sample query result for demonstration
                query_result = cursor.fetchall()

                # Create a DataFrame from the query result
                df = pd.DataFrame(query_result, columns=["Channel Name", "Video Name", "Comment Count"])

                # Create a selection box with options
                selected_option1 = st.selectbox("Select Chart Type", ["Scatter Plot", "Bar Chart",], key='chart_type_1')

                # Based on the selected option, display the corresponding plot

                if selected_option1 == "Scatter Plot":
                    scatter_fig = px.scatter(data_frame=df1, x="Channel Name", y="Video Name", color="Channel Name")
                    st.plotly_chart(scatter_fig)
                elif selected_option1 == "Bar Chart":
                    bar_fig = px.bar(data_frame=df1, x="Channel Name", y="Video Name", color="Channel Name")
                    st.plotly_chart(bar_fig)


            # Q2
            elif question_tosql == '2. Which channels have the most number of videos, and how many videos do they have?':

                cursor.execute("SELECT Channel_Name, Video_Count FROM channel ORDER BY Video_Count DESC;")
                result_2 = cursor.fetchall()
                df2 = pd.DataFrame(result_2, columns=['Channel Name', 'Video Count']).reset_index(drop=True)
                df2.index += 1
                st.dataframe(df2)

                # Sample query result for demonstration
                query_result = cursor.fetchall()

                # Create a DataFrame from the query result
                df = pd.DataFrame(query_result, columns=["Channel Name", "Video Name", "Channel Name"])

                # Create a selection box with options
                selected_option2 = st.selectbox("Select Chart Type", ["Scatter Plot", "Bar Chart",], key='chart_type_2')

                # Based on the selected option, display the corresponding plot

                if selected_option2 == "Scatter Plot":
                    scatter_fig = px.scatter(data_frame=df2, x="Channel Name", y="Video Count", color="Channel Name")
                    st.plotly_chart(scatter_fig)
                elif selected_option2 == "Bar Chart":
                    bar_fig = px.bar(data_frame=df2, x="Channel Name", y="Video Count", color="Channel Name")
                    st.plotly_chart(bar_fig)

            # Q3
            elif question_tosql == '3. What are the top 10 most viewed videos and their respective channels?':

                cursor.execute(
                    "SELECT channel.Channel_Name, video.Video_Name, video.View_Count FROM channel JOIN playlist ON channel.Channel_Id = playlist.Channel_Id JOIN video ON playlist.Playlist_Id = video.Playlist_Id ORDER BY video.View_Count DESC LIMIT 10;")
                result_3 = cursor.fetchall()
                df3 = pd.DataFrame(result_3, columns=['Channel Name', 'Video Name', 'View count']).reset_index(
                    drop=True)
                df3.index += 1
                st.dataframe(df3)

                # Sample query result for demonstration
                query_result = cursor.fetchall()

                # Create a DataFrame from the query result
                df = pd.DataFrame(query_result, columns=["Channel Name", "Video Name", "View count"])

                # Create a selection box with options
                selected_option3 = st.selectbox("Select Chart Type", ["Scatter Plot", "Bar Chart",], key='chart_type_3')

                # Based on the selected option, display the corresponding ploty

                if selected_option3 == "Scatter Plot":
                    scatter_fig = px.scatter(data_frame=df3, x="Channel Name", y="Video Name",
                                             color="View count")
                    st.plotly_chart(scatter_fig)
                elif selected_option3 == "Bar Chart":
                    bar_fig = px.bar(data_frame=df3, x="Channel Name", y="Video Name", color="View count")
                    st.plotly_chart(bar_fig)


            # Q4
            elif question_tosql == '4. How many comments were made on each video, and what are their corresponding video names?':
                cursor.execute(
                    "SELECT channel.Channel_Name, video.Video_Name, video.Comment_Count FROM channel JOIN playlist ON channel.Channel_Id = playlist.Channel_Id JOIN video ON playlist.Playlist_Id = video.Playlist_Id;")
                result_4 = cursor.fetchall()
                df4 = pd.DataFrame(result_4, columns=['Channel Name', 'Video Name', 'Comment count']).reset_index(
                    drop=True)
                df4.index += 1
                st.dataframe(df4)

                # Sample query result for demonstration
                query_result = cursor.fetchall()

                # Create a DataFrame from the query result
                df = pd.DataFrame(query_result, columns=["Channel Name", "Video Name", "Comment count"])

                # Create a selection box with options
                selected_option4 = st.selectbox("Select Chart Type", ["Scatter Plot", "Bar Chart",], key='chart_type_4')

                # Based on the selected option, display the corresponding ploty

                if selected_option4 == "Scatter Plot":
                    scatter_fig = px.scatter(data_frame=df4, x="Channel Name", y="Video Name",
                                             color="Comment count")
                    st.plotly_chart(scatter_fig)
                elif selected_option4 == "Bar Chart":
                    bar_fig = px.bar(data_frame=df4, x="Channel Name", y="Video Name", color="Comment count")
                    st.plotly_chart(bar_fig)


            # Q5
            elif question_tosql == '5. Which videos have the highest number of likes, and what are their corresponding channel names?':
                cursor.execute(
                    "SELECT channel.Channel_Name, video.Video_Name, video.Like_Count FROM channel JOIN playlist ON channel.Channel_Id = playlist.Channel_Id JOIN video ON playlist.Playlist_Id = video.Playlist_Id ORDER BY video.Like_Count DESC;")
                result_5 = cursor.fetchall()
                df5 = pd.DataFrame(result_5, columns=['Channel Name', 'Video Name', 'Like count']).reset_index(
                    drop=True)
                df5.index += 1
                st.dataframe(df5)

                # Sample query result for demonstration
                query_result = cursor.fetchall()

                # Create a DataFrame from the query result
                df = pd.DataFrame(query_result, columns=["Channel Name", "Video Name", "Like count"])

                # Create a selection box with options
                selected_option5 = st.selectbox("Select Chart Type", ["Scatter Plot", "Bar Chart",], key='chart_type_5')

                # Based on the selected option, display the corresponding ploty

                if selected_option5 == "Scatter Plot":
                    scatter_fig = px.scatter(data_frame=df5, x="Channel Name", y="Video Name",
                                             color="Like count")
                    st.plotly_chart(scatter_fig)
                elif selected_option5 == "Bar Chart":
                    bar_fig = px.bar(data_frame=df5, x="Channel Name", y="Video Name",
                                             color="Like count")
                    st.plotly_chart(bar_fig)


            # Q6
            elif question_tosql == '6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?':
                st.write(
                    '**Note:- In November 2021, YouTube removed the public dislike count from all of its videos.**')
                cursor.execute(
                    "SELECT channel.Channel_Name, video.Video_Name, video.Like_Count, video.Dislike_Count FROM channel JOIN playlist ON channel.Channel_Id = playlist.Channel_Id JOIN video ON playlist.Playlist_Id = video.Playlist_Id ORDER BY video.Like_Count DESC;")
                result_6 = cursor.fetchall()
                df6 = pd.DataFrame(result_6,
                                   columns=['Channel Name', 'Video Name', 'Like count', 'Dislike count']).reset_index(
                    drop=True)
                df6.index += 1
                st.dataframe(df6)

                # Sample query result for demonstration
                query_result = cursor.fetchall()

                # Create a DataFrame from the query result
                df = pd.DataFrame(query_result, columns=["Channel Name", "Video Name", "Like Count", "Dislike count"])

                # Create a selection box with options
                selected_option6 = st.selectbox("Select Chart Type", ["Scatter Plot", "Bar Chart",], key='chart_type_6')

                # Based on the selected option, display the corresponding ploty

                if selected_option6 == "Scatter Plot":
                    scatter_fig = px.scatter(data_frame=df6, x="Video Name", y="Like count", color="Channel Name")
                    st.plotly_chart(scatter_fig)
                elif selected_option6 == "Bar Chart":
                    bar_fig = px.bar(data_frame=df6, x="Video Name", y="Like count", color="Channel Name")
                    st.plotly_chart(bar_fig)

            # Q7
            elif question_tosql == '7. What is the total number of views for each channel, and what are their corresponding channel names?':

                cursor.execute("SELECT Channel_Name, Channel_Views FROM channel ORDER BY Channel_Views DESC;")
                result_7 = cursor.fetchall()
                df7 = pd.DataFrame(result_7, columns=['Channel Name', 'Total number of views']).reset_index(drop=True)
                df7.index += 1
                st.dataframe(df7)

                # Sample query result for demonstration
                query_result = cursor.fetchall()

                # Create a DataFrame from the query result
                df = pd.DataFrame(query_result, columns=["Channel Name", "Video Name", "Total number of views"])

                # Create a selection box with options
                selected_option7 = st.selectbox("Select Chart Type", ["Scatter Plot", "Bar Chart",], key='chart_type_7')

                # Based on the selected option, display the corresponding ploty

                if selected_option7 == "Scatter Plot":
                    scatter_fig = px.scatter(data_frame=df7, x="Total number of views", y="Channel Name",
                                             color="Total number of views")
                    st.plotly_chart(scatter_fig)
                elif selected_option7 == "Bar Chart":
                    bar_fig = px.bar(data_frame=df7, x="Channel Name", y="Total number of views",
                                             color="Channel Name")
                    st.plotly_chart(bar_fig)


            # Q8
            elif question_tosql == '8. What are the names of all the channels that have published videos in the year 2022?':
                cursor.execute(
                    "SELECT channel.Channel_Name, video.Video_Name, video.Published_date FROM channel JOIN playlist ON channel.Channel_Id = playlist.Channel_Id JOIN video ON playlist.Playlist_Id = video.Playlist_Id  WHERE EXTRACT(YEAR FROM Published_date) = 2022;")
                result_8 = cursor.fetchall()
                df8 = pd.DataFrame(result_8, columns=['Channel Name', 'Video Name', 'Year 2022 only']).reset_index(
                    drop=True)
                df8.index += 1
                st.dataframe(df8)

                # Sample query result for demonstration
                query_result = cursor.fetchall()

                # Create a DataFrame from the query result
                df = pd.DataFrame(query_result, columns=["Channel Name", "Video Name", "Year 2022 only"])

                # Create a selection box with options
                selected_option8 = st.selectbox("Select Chart Type", ["Scatter Plot", "Bar Chart",], key='chart_type_8')

                # Based on the selected option, display the corresponding ploty

                if selected_option8 == "Scatter Plot":
                    scatter_fig = px.scatter(data_frame=df8, x="Video Name", y="Year 2022 only", color="Channel Name")
                    st.plotly_chart(scatter_fig)
                elif selected_option8 == "Bar Chart":
                    bar_fig = px.bar(data_frame=df8, x="Video Name", y="Year 2022 only", color="Channel Name")
                    st.plotly_chart(bar_fig)


            # Q9
            elif question_tosql == '9. What is the average duration of all videos in each channel, and what are their corresponding channel names?':
                cursor.execute(
                    "SELECT channel.Channel_Name, TIME_FORMAT(SEC_TO_TIME(AVG(TIME_TO_SEC(TIME(video.Duration)))), '%H:%i:%s') AS duration  FROM channel JOIN playlist ON channel.Channel_Id = playlist.Channel_Id JOIN video ON playlist.Playlist_Id = video.Playlist_Id GROUP by Channel_Name ORDER BY duration DESC ;")
                result_9 = cursor.fetchall()
                df9 = pd.DataFrame(result_9,
                                   columns=['Channel Name', 'Average duration of videos (HH:MM:SS)']).reset_index(
                    drop=True)
                df9.index += 1
                st.dataframe(df9)

                # Sample query result for demonstration
                query_result = cursor.fetchall()

                # Create a DataFrame from the query result
                df = pd.DataFrame(query_result, columns=["Channel Name", "Video Name", "Average duration of videos (HH:MM:SS)"])

                # Create a selection box with options
                selected_option9 = st.selectbox("Select Chart Type", ["Scatter Plot", "Bar Chart"], key='chart_type_9')

                # Based on the selected option, display the corresponding ploty

                if selected_option9 == "Scatter Plot":
                    scatter_fig = px.scatter(data_frame=df9, x="Average duration of videos (HH:MM:SS)", y="Channel Name",
                                             color="Channel Name")
                    st.plotly_chart(scatter_fig)
                elif selected_option9 == "Bar Chart":
                    bar_fig = px.bar(data_frame=df9, x="Average duration of videos (HH:MM:SS)", y="Channel Name",
                                             color="Channel Name")
                    st.plotly_chart(bar_fig)


            # Q10
            elif question_tosql == '10. Which videos have the highest number of comments, and what are their corresponding channel names?':
                cursor.execute(
                    "SELECT channel.Channel_Name, video.Video_Name, video.Comment_Count FROM channel JOIN playlist ON channel.Channel_Id = playlist.Channel_Id JOIN video ON playlist.Playlist_Id = video.Playlist_Id ORDER BY video.Comment_Count DESC;")
                result_10 = cursor.fetchall()
                df10 = pd.DataFrame(result_10,
                                    columns=['Channel Name', 'Video Name', 'Number of comments']).reset_index(
                    drop=True)
                df10.index += 1
                st.dataframe(df10)

                # Create a selection box with options
                selected_option10 = st.selectbox("Select Chart Type", ["Scatter Plot", "Bar Chart"],
                                                 key='chart_type_10')

                # Based on the selected option, display the corresponding plot

                if selected_option10 == "Scatter Plot":
                    scatter_fig = px.scatter(data_frame=df10, x="Channel Name", y="Video Name",
                                             color="Number of comments")
                    st.plotly_chart(scatter_fig)
                elif selected_option10 == "Bar Chart":
                    bar_fig = px.bar(data_frame=df10, x="Channel Name", y="Video Name", color="Number of comments")
                    st.plotly_chart(bar_fig)


if __name__ == "__main__":
    main()
