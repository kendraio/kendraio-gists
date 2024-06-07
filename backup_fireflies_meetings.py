# %%
# Visit Fireflies.ai in a logged-in state and open the developer tools in your browser
# then go to https://app.fireflies.ai/notebook/all
# and look at the network tab in the developer tools
# identify the request to the URL https://app.fireflies.ai/api/v2/graphql
# copy the request headers and payload from the browser request, by right clicking on the request
# then select copy as fetch
# extract the headers from the fetch request
# or use the official Fireflies API to key a key to access the API,
# but note that it may have rate limits that prevent you from downloading all your data at once

# Copy the headers from the browser request here:
headers = {}

# Ensure you have the requests library installed by running `pip install requests`,
# then run this script like so: `python backup_fireflies_meetings.py`

import os
import random
from time import sleep
import requests

url = "https://app.fireflies.ai/api/v2/graphql"



get_meeting_graphql_payload = {
    "operationName": "fetchChannelMeetings",
    "variables": {"channelId": "all", "from": 0, "size": 400, "search": ""},
    "query": """query fetchChannelMeetings($from: Int!, $size: Int!, $channelId: String!, $search: String, $isPrivate: Boolean) {
        getChannelMeetings(
        from: $from
        size: $size
        channelId: $channelId
        search: $search
        isPrivate: $isPrivate
        ) {
        total
        meetings {
            parseId
            hasCaptions
            date
            owner
            title
            createdAt
            channelIds
            creator_email
            creatorProfile {
            picture
            name
            lastName
            firstName
            email
            __typename
            }
            privacy
            id
            users
            validAttendees
            durationMins
            duration
            allEmails
            audioOnly
            processMeetingStatus
            audioServiceMetadata {
            apiSource
            silentMeeting
            __typename
            }
            audio_url
            addedBy
            meetingExpirySettings {
            meetingTtl
            unit
            deletionTime
            __typename
            }
            __typename
        }
        __typename
        }
    }""",
}

fetch_meeting_notes_graphql_query_string = """
    fragment CoreAskFredFields on FredResponse {
            id
            question
            answer
            rating
            status
            rating
            meetingId
            answer
            privacy
            source
            __typename
        }
        query fetchNotepadMeeting($meetingNoteId: String!) {
            meetingNote(_id: $meetingNoteId) {
                _id
                transcriptParseId
                captions {
                    index
                    sentence
                    speaker_id
                    time
                    endTime
                    match
                    metrics {
                        word
                        category
                        __typename
                    }
                    sentiment
                    sentimentType
                    filterType
                    __typename
                }
                attendees {
                    email
                    displayName
                    __typename
                }
                title
                audio_url
                date
                parseId
                processMeetingStatus
                createdAt
                hasCaptions
                creator_email
                waveformData
                userPermission
                privacy
                owner
                audioOnly
                speakerMeta
                sentenceMeta
                paragraphMeta
                isGuestAccessEnabled
                labelMeta
                video_url
                txService
                defaultChannelAccess
                audioServiceMetadata {
                    silentMeeting
                    languageCode
                    preferredLanguage
                    __typename
                }
                addedBy
                allEmails
                fredQA {
                    ...CoreAskFredFields
                    __typename
                }
                durationMins
                meetingExpirySettings {
                    meetingTtl
                    unit
                    deletionTime
                    __typename
                }
                summaryStatus
                __typename
            }
    }"""


def random_sleep():
    # It's polite to sleep for a random amount of time between requests to avoid overloading the server
    sleep(random.uniform(0.2, 3.0))


def get_meetings():
    response = requests.post(url, headers=headers, json=get_meeting_graphql_payload)
    response.raise_for_status()

    data = response.json()
    meetings = data["data"]["getChannelMeetings"]["meetings"]

    results = []
    for meeting in meetings:
        result = {
            "title": meeting["title"],
            "date": meeting["date"],
            "id": meeting["id"],
        }
        results.append(result)

    return results


meetings = get_meetings()
for meeting in meetings:
    print(meeting)


# %%


def get_meeting_transcript(meeting_note_id):
    get_meeting_notes_graphql_query_payload = {
        "operationName": "fetchNotepadMeeting",
        "variables": {"meetingNoteId": meeting_note_id},
        "query": fetch_meeting_notes_graphql_query_string,
    }

    response = requests.post(
        url, headers=headers, json=get_meeting_notes_graphql_query_payload
    )
    response.raise_for_status()

    data = response.json()

    # save the json response to a file named by the meeting_note_id as a .json file:
    final_filename = f"{meeting_note_id}.json"
    with open(final_filename, "w") as f:
        f.write(response.text)

    captions = data["data"]["meetingNote"]["captions"]
    speakers = data["data"]["meetingNote"]["speakerMeta"]

    transcript_list = []
    for caption in captions:
        speaker_name = speakers.get(str(caption["speaker_id"]), "Unknown Speaker")
        time = caption["time"]
        sentence = caption["sentence"]
        transcript_list.append(f'{time}: {speaker_name} said: "{sentence}"')

    transcript = "\n".join(transcript_list)
    return transcript


# %%
# Test that we can get a transcript:
print(get_meeting_transcript(meetings[0]["id"]))


# %%

for meeting in meetings:
    print(meeting["date"], meeting["title"])
    transcript = get_meeting_transcript(meeting["id"])
    print(transcript)
    meeting["transcript"] = transcript
    # also we save a .txt file with the transcript, using the meeting date, title and id in the filename
    filename = f"{meeting['date']}_{meeting['title']}_{meeting['id']}"
    # only allow alphanumeric characters, spaces and underscores in the filename because other characters are not allowed in filenames
    # and cause issues with saving files
    safe_filename = "".join(c if c.isalnum() or c in " _" else "_" for c in filename)
    safe_filename += ".txt"
    with open(safe_filename, "w") as f:
        f.write(transcript)
    random_sleep()
# %%


# This potentially more efficient way didn't work, it caused a 403 issue, the MP3 URL paths were observed to be different from the JSON response and the MP3 URLs were not accessible:
def get_meeting_audio_urls():
    payload = {
        "operationName": "fetchChannelMeetings",
        "variables": {"channelId": "all", "from": 0, "size": 200, "search": ""},
        "query": """query fetchChannelMeetings($from: Int!, $size: Int!, $channelId: String!, $search: String, $isPrivate: Boolean) {
          getChannelMeetings(
            from: $from
            size: $size
            channelId: $channelId
            search: $search
            isPrivate: $isPrivate
          ) {
            total
            meetings {
              id
              date
              audio_url
            }
          }
        }""",
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    data = response.json()
    meetings = data["data"]["getChannelMeetings"]["meetings"]

    results = []
    for meeting in meetings:
        result = {
            "id": meeting["id"],
            "date": meeting["date"],
            "audio_url": meeting["audio_url"],
        }
        results.append(result)

    return results


# %%
# This was repurposed from the get_meeting_transcript function to get the audio url, because that did provide working audio URLs:
def get_meeting_audio_url(meeting_note_id):
    payload = {
        "operationName": "fetchNotepadMeeting",
        "variables": {"meetingNoteId": meeting_note_id},
        "query": fetch_meeting_notes_graphql_query_string,
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()

    # get the audio_url and return it
    audio_url = data["data"]["meetingNote"]["audio_url"]
    return audio_url


for meeting in meetings:
    # Make a filename string for the audio file, using the meeting date and id from the meeting object
    audio_filename = f"{meeting['date']}_{meeting['id']}"
    # Certain characters are not allowed in filenames, so we replace them with underscores:
    safe_audio_filename = "".join(
        c if c.isalnum() or c in " _" else "_" for c in audio_filename
    )
    safe_audio_filename += ".mp3"

    file_exists = os.path.exists(safe_audio_filename)
    if not file_exists:
        print(meeting["date"], meeting["title"])
        audio_url = get_meeting_audio_url(meeting["id"])
        print(audio_url)
        meeting["audio_url"] = audio_url

        with open(safe_audio_filename, "wb") as f:
            audio_response = requests.get(audio_url, headers=headers)
            audio_response.raise_for_status()
            f.write(audio_response.content)
        random_sleep()
