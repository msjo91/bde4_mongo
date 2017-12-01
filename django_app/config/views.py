"""
Main index
"""

from django.shortcuts import redirect


def index(request):
    """
    If user signs in, redirect to post:list
    유저가 로그인했을 경우, post:list로 이동
    If not signed in, redirect to member:signup
    로그인하지 않았을 경우, member:signup으로 이동
    """
    if request.user.is_authenticated:
        return redirect('post:list')
    else:
        return redirect('member:signup')
