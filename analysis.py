

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

from googleapiclient.discovery import build


api_key = 'AIzaSyAz2IRFGu0JHqjnQoRCQaAuujhhY1W5djk'


api_service_name = "youtube"
api_version = "v3"

# Get credentials and create an API client

youtube = build(
            'youtube', 'v3',
            developerKey =api_key)



request = youtube.channels().list(
    part="statistics",
    forUsername="schafer5"
)



response = request.execute()
