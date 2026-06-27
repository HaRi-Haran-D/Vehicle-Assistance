import razorpay
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponse
from .models import Payment, Invoice
from assistance.models import ServiceRequest
import io
from reportlab.pdfgen import canvas
from django.core.files.base import ContentFile

class CreatePaymentView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        service_request = get_object_or_404(ServiceRequest, pk=pk)
        
        # Calculate amount from repair details (ensure it exists)
        if hasattr(service_request, 'repair_details'):
            amount = int(service_request.repair_details.total_cost() * 100) # Razorpay works in paise
        else:
            amount = 10000 # Default 100 Rs if no details
            
        client = razorpay.Client(auth=(getattr(settings, 'RAZORPAY_KEY_ID', 'test_key'), getattr(settings, 'RAZORPAY_KEY_SECRET', 'test_secret')))
        
        try:
            payment_data = {
                'amount': amount,
                'currency': 'INR',
                'receipt': f'receipt_{service_request.id}',
                'payment_capture': 1
            }
            order = client.order.create(data=payment_data)
            
            payment, created = Payment.objects.get_or_create(
                service_request=service_request,
                defaults={'amount': amount / 100, 'razorpay_order_id': order['id']}
            )
            if not created:
                payment.razorpay_order_id = order['id']
                payment.amount = amount / 100
                payment.save()
                
            context = {
                'order_id': order['id'],
                'amount': amount,
                'key_id': getattr(settings, 'RAZORPAY_KEY_ID', 'test_key'),
                'service_request': service_request
            }
            return render(request, 'payments/payment_form.html', context)
        except Exception as e:
            messages.error(request, f"Error initializing payment: {e}")
            return redirect('request_detail', pk=service_request.id)

class PaymentSuccessView(View):
    def post(self, request, *args, **kwargs):
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')
        
        try:
            payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
            payment.razorpay_payment_id = razorpay_payment_id
            payment.razorpay_signature = razorpay_signature
            payment.status = 'SUCCESS'
            payment.save()
            
            # Update service request status
            service_request = payment.service_request
            service_request.status = 'PAID'
            service_request.save()
            
            messages.success(request, 'Payment successful!')
            return redirect('generate_invoice', pk=service_request.id)
        except Payment.DoesNotExist:
            messages.error(request, 'Payment record not found.')
            return redirect('customer_dashboard')

class GenerateInvoiceView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        service_request = get_object_or_404(ServiceRequest, pk=pk)
        
        # Simple PDF generation using reportlab
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(100, 800, f"Invoice for Service Request #{service_request.id}")
        p.drawString(100, 780, f"Customer: {service_request.customer.username}")
        if service_request.mechanic:
            p.drawString(100, 760, f"Mechanic: {service_request.mechanic.username}")
        if hasattr(service_request, 'repair_details'):
            p.drawString(100, 740, f"Total Amount: Rs {service_request.repair_details.total_cost()}")
        p.showPage()
        p.save()
        
        pdf = buffer.getvalue()
        buffer.close()
        
        invoice_number = f"INV-{service_request.id}-001"
        invoice, created = Invoice.objects.get_or_create(
            service_request=service_request,
            defaults={'invoice_number': invoice_number}
        )
        invoice.pdf_file.save(f'{invoice_number}.pdf', ContentFile(pdf))
        
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{invoice_number}.pdf"'
        return response
