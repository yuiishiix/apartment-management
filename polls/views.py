from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Poll, PollOption
from .serializers import PollSerializer

class PollListView(APIView):
    def get(self, request):
        poll = Poll.objects.first()  # You can adjust this to fetch polls differently
        serializer = PollSerializer(poll)
        return Response(serializer.data)

class VotePollView(APIView):
    def post(self, request, pk):
        poll = Poll.objects.get(id=pk)
        option_id = request.data.get('option_id')

        try:
            option = PollOption.objects.get(id=option_id, poll=poll)
            option.votes += 1
            option.save()
            return Response({"message": "Vote cast successfully!"}, status=status.HTTP_200_OK)
        except PollOption.DoesNotExist:
            return Response({"error": "Invalid option"}, status=status.HTTP_400_BAD_REQUEST)
