from rest_framework import serializers
from accounts.models import User, CustomerProfile
from vehicles.models import Vehicle
from mechanics.models import MechanicProfile
from assistance.models import ServiceRequest, ServiceImage, RepairDetails
from reviews.models import Review

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'role', 'first_name', 'last_name']

class CustomerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = CustomerProfile
        fields = '__all__'

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'
        read_only_fields = ['owner']

class MechanicProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = MechanicProfile
        fields = '__all__'

class ServiceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceImage
        fields = ['id', 'image', 'image_type', 'uploaded_at']

class RepairDetailsSerializer(serializers.ModelSerializer):
    total_cost = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = RepairDetails
        fields = '__all__'

class ServiceRequestSerializer(serializers.ModelSerializer):
    images = ServiceImageSerializer(many=True, read_only=True)
    repair_details = RepairDetailsSerializer(read_only=True)
    customer = UserSerializer(read_only=True)
    mechanic = UserSerializer(read_only=True)
    
    class Meta:
        model = ServiceRequest
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)
    mechanic = UserSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['customer', 'mechanic', 'service_request']
