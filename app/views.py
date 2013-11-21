from pprint import pprint
from django.shortcuts import render
from django.http import Http404

from forms import AccountForm
from models import Message, Account
from ajax import JsonResponse


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'login.html', locals())

    try:
        account = Account.objects.get(user=request.user)
    except Account.DoesNotExist:
        account = Account(user=request.user)

    if request.POST:
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            account = form.save()
    else:
        form = AccountForm(instance=account)

    messages = Message.objects.all()[:50]
    social = request.user.social_auth.get()
    twitter = social.extra_data
    return render(request, 'index.html', locals())


def poll(request):
    if not request.user.is_authenticated():
        raise Http404

    try:
        account = Account.objects.get(user=request.user)
    except Account.DoesNotExist:
        return JsonResponse(None)

    return JsonResponse({
        "status": account.status()
    })
