from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.conf import settings

from .models import Subscription, EntryRelation
from .serializers import SubscriptionSerializer, EntryRelationSerializer


class SubscriptionViewSet(viewsets.mixins.CreateModelMixin,
                          viewsets.mixins.RetrieveModelMixin,
                          viewsets.mixins.DestroyModelMixin,
                          viewsets.mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    """
    API endpoint that allows subscriptions to be viewed or edited.
    """
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super(SubscriptionViewSet, self).dispatch(*args, **kwargs)

    def create(self, request, *args, **kwargs):

        subscription_count = Subscription.objects.filter(user=request.user).count()

        if hasattr(request.user, 'userstatus'):
            max_subscriptions = request.user.userstatus.max_subscriptions
        else:
            max_subscriptions = settings.NON_PREMIUM_MAX_SUBSCRIPTIONS

        if subscription_count >= max_subscriptions:
            content = {
                'detail': "Maximum subscriptions reached.",
                'is_premium': 1 if hasattr(request.user, 'userstatus') and request.user.userstatus.is_premium else 0,
                }

            return Response(content, status=status.HTTP_403_FORBIDDEN)

        return super(SubscriptionViewSet, self).create(request, *args, **kwargs)

    def get_queryset(self):
        return Subscription.objects.all().filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EntryRelationViewSet(viewsets.mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    """
    API endpoint that allows entries to be viewed or edited.
    """
    queryset = EntryRelation.objects.all()
    serializer_class = EntryRelationSerializer

    def get_object(self):
        try:
            return EntryRelation.objects.get(user=self.request.user)
        except ObjectDoesNotExist:
            return EntryRelation.objects.create(user=self.request.user)

    def list(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_queryset(self):
        return EntryRelation.objects.all().filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
