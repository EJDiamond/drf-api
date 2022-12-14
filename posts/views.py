# from django.http import Http404
from django.shortcuts import render
from rest_framework import generics, permissions
# from rest_framework.response import Response
# from rest_framework.views import APIView
from .models import Post
from .serializers import PostSerializer
from drf_api.permissions import IsOwnerOrReadOnly


class PostList(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    # ensures only the user instances can create posts
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    # this gets the edit form rendered in the browser
    serializer_class = PostSerializer
    # only post owner can edit or delete it
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.all()


    # this handles the case a post doesnt exist
    # def get_object(self, pk):
    #     try:
    #         # this tries to get a post by using the primary key
    #         post = Post.objects.get(pk=pk)
    #         # this makes sure the requests user has permission to edit or delete the post
    #         self.check_object_permissions(self.request, post)
    #         return post
    #     # if the post doesnt exist a 404 exception is raised
    #     except Post.DoesNotExist:
    #         raise Http404

    # # this retrieves a post by id
    # def get(self, request, pk):
    #     # this handles the post doesn't exist exception
    #     post = self.get_object(pk)
    #     # if an error isnt thrown we serialize that single post with the post serializer
    #     # the request is passed in the context obkect and then retrurn the serializers
    #     # data in the response.
    #     serializer = PostSerializer(post, context={'request': request})
    #     return Response(serializer.data)
    #     # remember to add the post detail view to the urls

    # # updating a post
    # def put(self, request, pk):
    #     # this handles the post doesnt exist error
    #     post = self.get_object(pk)
    #     # call serializer with the post instance, the request update data and the
    #     # request itself inside the context object
    #     serializer = PostSerializer(
    #         post, data=request.data, context={'request': request})
    #     # if the data is valid it is saved to the database and sent back in the response.
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     # if not valid a responds with a serializer error
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # deleting a post
    # def delete(self, request, pk):
    #     post = self.get_object(pk)
    #     post.delete()
    #     return Response(
    #         status=status.HTTP_204_NO_CONTENT
    #     )
