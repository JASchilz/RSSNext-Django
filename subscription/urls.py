from django.conf.urls import url, include
from rest_framework import routers

from .views import SubscriptionViewSet, EntryRelationViewSet

router = routers.DefaultRouter()
router.register(r'subscriptions', SubscriptionViewSet)
router.register(r'entries', EntryRelationViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),  # API routing
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]