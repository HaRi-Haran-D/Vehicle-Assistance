from django.http import JsonResponse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from .models import Message
from assistance.models import ServiceRequest
from django.utils.dateparse import parse_datetime

class SendMessageView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        service_request = get_object_or_404(ServiceRequest, pk=pk)
        content = request.POST.get('content')
        
        # Determine receiver
        if request.user == service_request.customer:
            receiver = service_request.mechanic
        elif request.user == service_request.mechanic:
            receiver = service_request.customer
        else:
            return JsonResponse({'error': 'Unauthorized'}, status=403)
            
        if not receiver:
            return JsonResponse({'error': 'No recipient available'}, status=400)
            
        if content:
            message = Message.objects.create(
                service_request=service_request,
                sender=request.user,
                receiver=receiver,
                content=content
            )
            return JsonResponse({
                'status': 'success',
                'message': {
                    'sender': message.sender.username,
                    'content': message.content,
                    'timestamp': message.timestamp.isoformat()
                }
            })
        return JsonResponse({'error': 'Empty content'}, status=400)

class GetMessagesView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        service_request = get_object_or_404(ServiceRequest, pk=pk)
        
        if request.user != service_request.customer and request.user != service_request.mechanic:
            return JsonResponse({'error': 'Unauthorized'}, status=403)
            
        last_timestamp = request.GET.get('last_timestamp')
        
        messages_qs = Message.objects.filter(service_request=service_request)
        if last_timestamp:
            dt = parse_datetime(last_timestamp)
            if dt:
                messages_qs = messages_qs.filter(timestamp__gt=dt)
                
        # Mark as read for received messages
        unread = messages_qs.filter(receiver=request.user, is_read=False)
        unread.update(is_read=True)
        
        data = []
        for msg in messages_qs:
            data.append({
                'sender': msg.sender.username,
                'is_me': msg.sender == request.user,
                'content': msg.content,
                'timestamp': msg.timestamp.isoformat()
            })
            
        return JsonResponse({'messages': data})
