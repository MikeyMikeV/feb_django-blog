from django.shortcuts import render, redirect
from .forms import SignUpForm, User
from django.contrib.auth import logout, authenticate, login


def create_user(request):
    if request.method != "POST":
        form = SignUpForm()
    else:
        form = SignUpForm(request.POST)
        if form.is_valid():
            user: User = form.save(commit=False)
            user.is_active = False
            user.save()
            send_activation_email(user, request)
            return redirect("login")
    context = {
        "form": form
    }
    return render(request, "create_user.html", context)

def log_out(request):
    logout(request)
    return redirect('login')


from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import  render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from .tokens import TokenGenerator
from django.http import HttpResponse

account_activation_token = TokenGenerator()

def send_activation_email(user, request):
    current_site = get_current_site(request)
    mail_subject = "Подтвердите вашу почту"
    message = render_to_string(
        template_name="registration/acc_activation_email.html",
        context={
            "username":user.username,
            "domain": current_site,
            "user_id": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user)
        }
    )
    email = EmailMessage(mail_subject, message, to=[user.email])
    email.send()

def activate(request,user_id, token):
    try:
        uid = force_str(urlsafe_base64_decode(user_id))
        user = User.objects.get(pk = uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    return HttpResponse("<h1>Активация не пройдена!</h1>")