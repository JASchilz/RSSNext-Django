from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required

from allauth.account.views import logout, login

from .views import LoginAndSignUpFormView, view_that_asks_for_money
from .decorators import anonymous_required

urlpatterns = patterns('',

    url(r'^$', anonymous_required(LoginAndSignUpFormView.as_view()), name="login"),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/', login_required(TemplateView.as_view(template_name="rssnext/home.html"), login_url="/"), name='home'),
    url(r'^next/', login_required(TemplateView.as_view(template_name="rssnext/next.html"), login_url="/"), name='next'),

    url(r'^accounts/premium/', login_required(view_that_asks_for_money, login_url="/"), name='premium'),

    url(r'^accounts/logout', logout, name="logout"),  # Hack for feedreader

    url(r'^accounts/', include('allauth.urls')),

    url(r'^feedreader/', include('feedreader.urls', namespace="feedreader")),

    url(r'^payments/paypal/', include('paypal.standard.ipn.urls')),

    url(r'^v1/', include('subscription.urls')),
)
