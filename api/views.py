from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from accounts.models import User, CustomerProfile
from vehicles.models import Vehicle
from mechanics.models import MechanicProfile
from assistance.models import ServiceRequest
from reviews.models import Review
from .serializers import (
    UserSerializer, CustomerProfileSerializer, VehicleSerializer,
    MechanicProfileSerializer, ServiceRequestSerializer, ReviewSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class VehicleViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Vehicle.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class MechanicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MechanicProfile.objects.all()
    serializer_class = MechanicProfileSerializer
    permission_classes = [permissions.AllowAny]

class ServiceRequestViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_mechanic():
            return ServiceRequest.objects.filter(mechanic=user)
        return ServiceRequest.objects.filter(customer=user)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        service_request_id = self.request.data.get('service_request')
        try:
            service_request = ServiceRequest.objects.get(id=service_request_id)
            serializer.save(
                customer=self.request.user,
                mechanic=service_request.mechanic,
                service_request=service_request
            )
        except ServiceRequest.DoesNotExist:
            return Response({'error': 'Service Request not found'}, status=status.HTTP_404_NOT_FOUND)
