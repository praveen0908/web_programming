import requests

try:
    from django.contrib.auth import authenticate, login
    from django.shortcuts import redirect, render
except ImportError:
    authenticate = login = render = redirect = print


def login_using_recaptcha(request):
    # Enter your recaptcha secret key here
    secret_key = "secretKey"
    url = "https://www.google.com/recaptcha/api/siteverify"

    # when method is not POST, direct user to login page
    if request.method != "POST":
        return render(request, "login.html")

    # from the frontend, get username, password, and client_key
    username = request.POST.get("username")
    password = request.POST.get("password")
    client_key = request.POST.get("g-recaptcha-response")

    # post recaptcha response to Google's recaptcha api
    response = requests.post(url, data={"secret": secret_key, "response": client_key})
    # if the recaptcha api verified our keys
    if response.json().get("success", False):
        # authenticate the user
        user_in_database = authenticate(request, username=username, password=password)
        if user_in_database:
            login(request, user_in_database)
            return redirect("/your-webpage")
    return render(request, "login.html")