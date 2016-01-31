"""
Those Django models relating
"""

from datetime import timedelta

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.utils import timezone
from django.conf import settings

from feedreader.models import Feed, Entry

from paypal.standard.ipn.signals import payment_was_successful, payment_was_flagged


class Subscription(models.Model):
    """
    A relation between a feed and a user.
    """

    feed = models.ForeignKey(Feed)
    user = models.ForeignKey(User)

    class Meta(object):
        """
        Users may not be double subscribed to a feed.
        """
        unique_together = ("feed", "user")

    @property
    def url(self):
        """
        :return: the url of the subscription's feed.
        """
        return self.feed.xml_url

    def __str__(self):
        """
        :return:
        """
        return str(self.user) + " subscribed to " + str(self.feed.title)


class UserStatus(models.Model):
    """
    A record of premium status for each user.
    """

    user = models.OneToOneField(User)

    premium_until = models.DateTimeField(null=True)

    @property
    def is_premium(self):
        """
        :return: whether or not the user is currently in premium status
        """
        return self.premium_until and self.premium_until > timezone.now()

    @property
    def max_subscriptions(self):
        """
        :return: how many subscriptions the user is allowed to have
        """
        if self.is_premium:
            return settings.PREMIUM_MAX_SUBSCRIPTIONS
        else:
            return 20


class EntryRelation(models.Model):
    """
    A record of the most recently read entry for each user.
    """

    user = models.OneToOneField(User)

    last_entry = models.ForeignKey(Entry, null=True, related_name="last_entry")
    next_entry = models.ForeignKey(Entry, null=True, related_name="next_entries")

    next_sponsored_entry = models.ForeignKey(
        Entry,
        null=True,
        related_name="next_sponsored_entry"
    )

    next_sponsored_delivery_date = models.DateTimeField(null=True)

    extra_entries = models.ManyToManyField(Entry, related_name="extra_entries")
    announcement_entries = models.ManyToManyField(Entry, related_name="announcement_entries")

    def _next_entry(self):
        """
        :return: the next subscription entry to be provided to the user.
        """

        if self.next_entry is not None:
            this_entry = self.next_entry
            self.next_entry = None

            return this_entry

        try:
            this_users_feeds = Entry.objects.filter(feed__subscription__user=self.user)
            if self.last_entry is None:
                this_entry = this_users_feeds.earliest('published_time')

            else:
                this_entry = this_users_feeds.\
                    filter(published_time__gt=self.last_entry.published_time).\
                    earliest('published_time')

        except ObjectDoesNotExist:
            this_entry = None

        return this_entry

    def get_next_entry(self):
        """
        :return: the next subscription, or sponsored entry to be provided to
        the user.
        """

        this_entry = None

        for entry_list in [self.announcement_entries, self.extra_entries]:
            if entry_list.exists():
                this_entry = entry_list.first()
                entry_list.remove(this_entry)

        if this_entry is None:
            this_entry = self._next_entry()

        if this_entry is None:
            raise Http404
        else:
            self.last_entry = this_entry
            self.save()
            return this_entry


def show_me_the_money(sender, **kwargs):  # pylint: disable=unused-arguments
    """
    Process a PayPal payment for premium status.

    :param sender: the PayPal object containing the payment information
    :return: None
    """
    ipn_obj = sender
    # You need to check 'payment_status' of the IPN

    if ipn_obj.payment_status == "Completed":

        user = User.objects.get(id=int(ipn_obj.custom))

        try:
            status = UserStatus.objects.get(user=user)
        except ObjectDoesNotExist:
            status = UserStatus.objects.create(user=user)

        if status.premium_until is None or status.premium_until < timezone.now():
            status.premium_until = timezone.now() + timedelta(weeks=52)
        else:
            status.premium_until += timedelta(weeks=52)

        status.save()

    else:
        pass

payment_was_successful.connect(show_me_the_money)
payment_was_flagged.connect(show_me_the_money)


