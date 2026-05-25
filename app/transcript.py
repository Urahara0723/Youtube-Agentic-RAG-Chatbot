import re
from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url: str) -> str:
    """
    Extract YouTube video ID from URL.
    """

    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11})"

    match = re.search(pattern, url)

    if not match:
        raise ValueError("Invalid YouTube URL")

    return match.group(1)


def get_transcript(video_id: str) -> str:
    """
    Fetch transcript from YouTube video.
    """

    api = YouTubeTranscriptApi()

    transcript = api.fetch(video_id)

    full_text = " ".join([snippet.text for snippet in transcript.snippets])

    return full_text
