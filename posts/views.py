from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post
from .serializers import PostSerializer


class PostList(APIView):
    serializer_class = PostSerializer
    # ensures only the user instances can create posts
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]

    def get(self, request):
        # retrieve all post instances from the database
        posts = Post.objects.all()
        # serialize them and pass many=true with the request in the context object
        serializer = PostSerializer(
            posts, many=True, context={'request': request}
        )
        # return serialized data in the response
        return Response(serializer.data)

    def post(self, request):
        # deserialize post data passing in whatever the user sends in the request itself in the context object
        serializer = PostSerializer(
            data=request.data, context={'request': request}
        )
        # if data is valid save the post and associate it with the current user
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )
