from dotenv import load_dotenv
import os

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser

import sys
import requests
import base64
import json
import logging


load_dotenv()

developer_key = os.getenv('YOUTUBE_API_KEY')

def build_youtube_search():
  DEVELOPER_KEY = developer_key
  YOUTUBE_API_SERVICE_NAME="youtube"
  YOUTUBE_API_VERSION="v3"
  return build(YOUTUBE_API_SERVICE_NAME,YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

def get_search_response(youtube, query):
  search_response = youtube.search().list(
    q = query,
    order = "relevance",
    part = "snippet",
    maxResults = 1
    ).execute()
  return search_response

def get_video_info(search_response):
  result_json = {}
  idx =0
  for item in search_response['items']:
    if item['id']['kind'] == 'youtube#video':
      result_json[idx] = info_to_dict(item['id']['videoId'], item['snippet']['title'], item['snippet']['description'], item['snippet']['thumbnails']['medium']['url'])
      idx += 1
  return result_json

def info_to_dict(videoId, title, description, url):
  result = {
      "videoId": videoId,
      "title": title,
      "description": description,
      "url": url
  }
  return result

def main(query):
    youtube = build_youtube_search()
    search_response = get_search_response(youtube, query)
    video_info = get_video_info(search_response)
    
    return video_info