from django.views.generic import FormView
from django.template import RequestContext

from allauth.account.forms import SignupForm, LoginForm
from allauth.account.views import complete_signup, app_settings


class LoginAndSignUpFormView(FormView):

    template_name = "account/login.html"
    success_url = "/home/"

    def get_context_data(self, **kwargs):
        context = super(LoginAndSignUpFormView, self).get_context_data(**kwargs)

        if "login_form" not in context:
            context["login_form"] = LoginForm()
        if "signup_form" not in context:
            context["signup_form"] = SignupForm()

        return context

    def get(self, request, *args, **kwargs):
        # form_class = self.get_form_class()
        # form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        form_name = request.POST.get('form_name', "")
        if form_name == "login_form":
            self.form_class = LoginForm
        elif form_name == "signup_form":
            self.form_class = SignupForm

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        """
        If the form is invalid, re-render the context data with the
        data-filled form and errors.
        """
        if self.get_form_class() == LoginForm:
            return self.render_to_response(self.get_context_data(login_form=form))
        elif self.get_form_class() == SignupForm:
            return self.render_to_response(self.get_context_data(signup_form=form))

    def form_valid(self, form):

        if self.get_form_class() == LoginForm:
            success_url = self.get_success_url()
            return form.login(self.request, redirect_url=success_url)

        elif self.get_form_class() == SignupForm:
            user = form.save(self.request)
            return complete_signup(self.request, user,
                                   app_settings.EMAIL_VERIFICATION,
                                   self.get_success_url())

from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def view_that_asks_for_money(request):

    # What you want the button to do.
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": "3.50",
        "item_name": "RSSNext - 1 Year Premium Upgrade",
        # "invoice": "unique-invoice-id",
        "notify_url": request.scheme + "://" + request.get_host() + reverse('paypal-ipn'),
        "return_url": request.scheme + "://" + request.get_host() + reverse('premium') + "?referer=paypal&status=success",
        "cancel_return": request.scheme + "://" + request.get_host() + reverse('premium') + "?referer=paypal&status=cancel",
        "custom": request.user.id,

    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render_to_response("rssnext/premium.html", context, context_instance=RequestContext(request))





