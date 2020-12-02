from django.shortcuts import render
from django.http.response import JsonResponse

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.parsers import JSONParser

from .serializers import PostSerializer
from .models import Post

# Create your views here.
@api_view(['GET','POST'])
def post(request):
    if request.method == 'GET': # post read all
        posts = Post.objects.all()
        posts_serializer = PostSerializer(posts, many=True)
        return JsonResponse(posts_serializer.data, safe=False)

    elif request.method == 'POST': # post write
        post = JSONParser().parse(request)
        post_serializer = PostSerializer(data=post)
        if post_serializer.is_valid():
            post_serializer.save()
            return JsonResponse(post_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def post_detail(request, id):
    try:
        posts = Post.objects.get(_id=id) #todo 잘 돌아가는지 테스트
    except Post.DoesNotExist:
        return JsonResponse({'message': '블로그 id의 내용이 없습니다.'},
                            status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET': # post read detail
        post_serializer = PostSerializer(posts, many=True)
        return JsonResponse(post_serializer.data, safe=False)
    elif request.method == 'PUT': # post edit
        post_data = JSONParser().parse(request)
        post_serializer = PostSerializer(posts, data=post_data)
        if post_serializer.is_valid():
            post_serializer.save()
            return JsonResponse(post_serializer.data)
        return JsonResponse(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        posts.delete()
        return JsonResponse({'message': '블로그 내용이 삭제되었습니다.'},
                            status=status.HTTP_204_NO_CONTENT)
