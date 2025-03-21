from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from tenants.models import Tenant
from .serializers import UserRegistrationSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Start a transaction to ensure both User and Tenant are created together
                with transaction.atomic():
                    user = serializer.save()

                    # Create the Tenant instance associated with the user
                    Tenant.objects.create(user=user)

                    # Create JWT tokens for the user
                    refresh = RefreshToken.for_user(user)
                    access_token = refresh.access_token

                    return Response({
                        'access': str(access_token),
                        'refresh': str(refresh)
                    }, status=status.HTTP_201_CREATED)
            except Exception as e:
                print("Error during user registration:", str(e))
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        print("Serializer errors:", serializer.errors)  # Debugging line
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

