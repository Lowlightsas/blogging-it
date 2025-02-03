from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import ChatGroup
from django.contrib.auth.decorators import login_required

@login_required
def chat_view(request):
    chat_group = get_object_or_404(ChatGroup, group_name='public-chat')
    chat_messages = chat_group.chat_messages.all()[:30]

    return render(request,'chat.html', {'chat_messages': chat_messages})