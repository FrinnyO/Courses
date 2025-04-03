from rest_framework import serializers


def validate_video_link(link):
    if "youtube.com" not in link:
        raise serializers.ValidationError("Link must be from youtube.com")
