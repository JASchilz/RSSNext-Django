from django.contrib.auth.models import User, Group
from rest_framework import serializers
from feedreader.models import Feed
from django.core.exceptions import ObjectDoesNotExist

import urllib

from .models import Subscription, EntryRelation


class SubscriptionSerializer(serializers.Serializer):

    id = serializers.ReadOnlyField()
    url = serializers.URLField()

    title = serializers.SerializerMethodField()

    def create(self, validated_data):
        # Find whether there is already a feed with this url

        try:
            feed = Feed.objects.get(xml_url=validated_data["url"])
        except ObjectDoesNotExist:
            feed = Feed.objects.create(xml_url=validated_data["url"])

            if feed.title is None:
                feed.title = validated_data["url"]

        return Subscription.objects.create(feed=feed,
                                           user=validated_data["user"])

    def get_title(self, obj):
        return obj.feed.title


class EntryRelationSerializer(serializers.Serializer):

    link = serializers.SerializerMethodField()

    # def create(self, validated_data):
    #     # Find whether there is already a feed with this url
    #
    #     try:
    #         feed = Feed.objects.get(xml_url=validated_data["url"])
    #     except ObjectDoesNotExist:
    #         feed = Feed.objects.create(xml_url=validated_data["url"])
    #
    #     return Subscription.objects.create(feed=feed,
    #                                        user=validated_data["user"])

    def get_link(self, obj):
        try:
            return obj.get_next_entry().link
        except AttributeError:
            return None