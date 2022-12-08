"""
    A library of functions to get Youtube captions and process them for research.
"""
import random
import math
import concurrent.futures
from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd
import requests
import re
import json
import numpy as np

from Video import Video


def get_video_info(file=""):
    """
        get_video_info
            Parse json file and get video ids and categories
        Parameters:
            file: json file to get extract information from
        Returns:
            List of video objects with video id and categories included. Transcripts are not included
    """
    # Temporary variables
    video_list = []

    # Open json file...
    with open(file) as file:
        data = json.load(file)                              # Load json data into object

        categories = data["vocabulary"]                     # Get categories data
        videos = data["videos"]                             # Get video data

    # For each video in the json file...
    for video_id in videos:
        temp_cats = videos[video_id]                        # List of categories from the video
        vid_cats = []                                       # Empty list to add word categories to

        # For each category the video is tagged as...
        for cat in temp_cats:
            vid_cats.append(categories[str(cat)])           # Add the category as a word

        new_video = Video(str(video_id), vid_cats, "")      # Create video object with video information

        video_list.append(new_video)                        # Add video to list of videos

    # print(str(len(video_list)) + " total videos")           # Print number of videos found
    return video_list


def find_proxy(proxy_list=[{"http": ""}]):
    """
        find_proxy
            Randomly get an ip from a list of proxy servers to avoid being ip banned
        Parameters:
            proxy_list: List of proxies to randomly find one from
        Returns:
            proxy: Random proxy server from given list
    """
    return proxy_list[random.randint(0, len(proxy_list) - 1)]   # Return random proxy from given list


def update_transcript(proxy={}, video=Video):
    """
        update_transcript
            Use proxy server to get transcript of video
        Parameters:
            proxy: Dictionary mapping of http or https proxies
            video: Video object to update with transcript
        Returns:
            video: Video object with transcript updated if one was found
    """
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video.id, proxies=proxy)
    except:
        return video
    else:
        text = ''

        # Change dictionary to pandas DataFrame
        transcript_df = pd.DataFrame(transcript)

        # Combine entire column of text into a single cell dataframe
        for row in transcript_df['text']:
            text += row + " "

        video.transcript = text

    return video


def update_transcripts_in_parallel(proxies=[{"": ""}], videos=[Video], num_workers=int):
    """
        update_transcripts_in_parallel
            Uses ThreadPoolExecutor to get multiple transcripts at once and return them
        Parameters:
            proxies: List of proxy servers used to make requests to Youtube
            videos: List of video objects, when passed to function IDs and categories should be filled out but transcripts should be empty.
            num_worker: Number of simultaneous requests to be made to Youtube. Each request will choose a random proxy server from the list
        Returns:
            Original list of video objects but with included transcripts
    """
    # Temporary video list
    video_list = []
    count = 0

    # Using ThreadPoolExecutor...
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        # For each video given submit a task to the ThreadPoolExecutor
        future_to_video = {executor.submit(update_transcript, find_proxy(proxies), video): video for video in videos}

        # As each task is completed...
        for future in concurrent.futures.as_completed(future_to_video):
            count += 1

            # If the result in None do not save the video, but if it has a transcript save the video to a list.
            try:
                if future.result().transcript != "":
                    print(f"%9d : Finished with video: %s, a transcript was found." % (count, future.result().id))
                    video_list.append(future.result())
                else:
                    print(f"%9d : Finished with video: %s, a transcript was NOT found." % (count, future.result().id))
            except Exception as exc:
                print(exc)


    # Return list of videos
    return video_list


def save_as_excel(videos=[Video], vids_per_file=int):
    """
        save_as_excel
            Save a list of video objects as an excel file
        Parameters:
            videos: List of Videos to safe
            vids_per_file: Number of videos to put into each file

        Excel files are limited to about 1 million rows
    """
    count = 1
    num_parts = math.ceil(len(videos) / vids_per_file)
    if num_parts < 1:
        num_parts = 1
    splits = np.array_split(videos, num_parts)    # Split video list into parts of 1 million video per excel file

    # Save dataframes as files
    for df_array in splits:
        df = pd.DataFrame.from_records([s.to_dict() for s in df_array])     # Save list of videos as a dataframe
        print(df)
        df.to_excel(f'output_{count}.xlsx', header=True, index=False)       # Save dataframe to excel
        count += 1                                                          # Increment count
