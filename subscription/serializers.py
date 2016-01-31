# pylint: disable=no-self-use
"""
Django Rest Framework serialization for the RSSNext project
"""

from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from feedreader.models import Feed

from .models import Subscription


class SubscriptionSerializer(serializers.Serializer):
    """
    Django Rest Framework serialization for the Subscription model.
    """

    id = serializers.ReadOnlyField()
    url = serializers.URLField()

    title = serializers.SerializerMethodField()

    def create(self, validated_data):
        """
        Creates a subscription given a url, by creating the feed if it does
        not already exist.

        :param validated_data: the data supplied to this serializer
        :return: the new Subscription object
        """

        try:
            feed = Feed.objects.get(xml_url=validated_data["url"])
        except ObjectDoesNotExist:
            feed = Feed.objects.create(xml_url=validated_data["url"])

            if feed.title is None:
                feed.title = validated_data["url"]

        return Subscription.objects.create(feed=feed,
                                           user=validated_data["user"])

    def get_title(self, obj):
        """
        :return: the title of the feed to which this subscription relates
        """
        return obj.feed.title


class EntryRelationSerializer(serializers.Serializer):
    """
    Django Rest Framework serialization for the EntryRelation model.
    """

    link = serializers.SerializerMethodField()

    def get_link(self, obj):
        """
        :param obj: the object under serialization.
        :return: the link for the next entry under this entry relation
        """
        try:
            return obj.get_next_entry().link
        except AttributeError:
            return None
