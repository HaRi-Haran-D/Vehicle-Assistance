from django.shortcuts import redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Notification

class MarkAsReadView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        notification = Notification.objects.get(pk=pk, user=request.user)
        notification.is_read = True
        notification.save()
        if notification.link:
            return redirect(notification.link)
        return redirect('home')
