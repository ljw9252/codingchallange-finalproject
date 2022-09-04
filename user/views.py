from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from user.models import User

from .forms import LoginForm, RegisterForm

User = get_user_model()


def index(request):
    return render(request, "index.html")



def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/login")
    else:
        logout(request)
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    is_ok = False
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password")
            remember_me = form.cleaned_data.get("remember_me")
            msg = "올바른 유저ID와 패스워드를 입력하세요."
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                msg = "올바른 유저ID와 패스워드를 입력하세요."
            else:
                if user.check_password(raw_password):
                    msg = None
                    login(request, user)
                    is_ok = True
                    request.session["remember_me"] = remember_me
            return redirect('index')
    else:
        msg = None
        form = LoginForm()
    print("REMEMBER_ME: ", request.session.get("remember_me"))

    return render(request, "login.html", {"form": form, "msg": msg, "is_ok": is_ok})


def logout_view(request):
    # TODO: 3. /logout url을 입력하면 로그아웃 후 / 경로로 이동시켜주세요
    logout(request)						
    return HttpResponseRedirect("/")


# TODO: 8. user 목록은 로그인 유저만 접근 가능하게 해주세요
@login_required
def user_list_view(request):
    # TODO: 7. /users 에 user 목록을 출력해주세요
    page = int(request.GET.get("p", 2))
    users = User.objects.all().order_by("-id")
    # TODO: 9. user 목록은 pagination이 되게 해주세요
    paginator = Paginator(users, 2)
    users = paginator.get_page(page)
    return render(request, "users.html", {"users": users})
