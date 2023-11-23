from django.shortcuts import render, get_object_or_404
from .models import Blogs, Likes
from rest_framework.response import Response
from .serializers import AboutUserSerializer, GetBlogsSerializer, LikeSerializer
from rest_framework import generics, permissions, mixins, status
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError


class GetUserInformation(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = AboutUserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    


class BlogsList(generics.ListCreateAPIView):
    queryset = Blogs.objects.all().order_by('-id')
    serializer_class = GetBlogsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)


class BlogUpdate(generics.RetrieveUpdateAPIView):
    serializer_class = GetBlogsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        id = self.kwargs["pk"]
        obj = Blogs.objects.filter(pk=id)
        return obj
    
    def put(self, request, *args, **kwargs):
        obj = self.get_queryset()
        if obj.exists() and obj.first().posted_by == request.user:
            return self.update(request, *args, **kwargs)
        else:
            raise ValidationError("You cannot update other person's post !!")




class LikesCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        blog = Blogs.objects.get(pk=self.kwargs['pk'])
        return Likes.objects.filter(liked_by=user, blog=blog)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError("You have already voted for this post !!")
        serializer.save(liked_by=self.request.user, blog=Blogs.objects.get(pk=self.kwargs['pk']))
    
    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError("There is nothing to delete here ..")


class BlogDestroy(generics.RetrieveDestroyAPIView):
    queryset = Blogs.objects.all()
    serializer_class = GetBlogsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def delete(self, request, *args, **kwargs):
        post = Blogs.objects.filter(pk=kwargs['pk'], posted_by=self.request.user)
        if post.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError("You cannot delete other person's blog !!")