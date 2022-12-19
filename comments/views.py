from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render
from rest_framework import generics, permissions
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Comment
from .serializers import CommentSerializer, CommentDetailSerializer


# Extending the ListAPIView means we  won’t have to write the get method
# and the CreateAPIView takes  care of the post method
class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    # don’t  want anonymous users to comment
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # in DRF we set the queryset attribute, possible to filter  out some of the model instances.
    # make sure users can access and query only their own data
    queryset = Comment.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post']

    # make sure  comments are associated with a user upon creation.
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    # In order not to have to send  the post id every time I want to edit a comment
    serializer_class = CommentDetailSerializer
    queryset = Comment.objects.all()
