from django.http.response import JsonResponse

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.parsers import JSONParser

from .serializers import PostMakeSerializer, PostReadSerializer
from .models import Post
from .mongo import MongoDbManager


# post_make_* 은 포스트을 만들기 위한 최소의 직렬화 ('title', 'body', 'tags')
# post_read_* 은 포스트를 읽기 위한 모델의 전부다.. ('_id', 'title', 'body', 'tags','published_date')



@api_view(['GET','POST'])
def post(request):
    if request.method == 'GET': # post read all
        posts = Post.objects.all()
        posts_read_serializer = PostReadSerializer(posts, many=True)
        return JsonResponse(posts_read_serializer.data, safe=False)

    elif request.method == 'POST': # post write
        posts = JSONParser().parse(request)
        post_make_serializer = PostMakeSerializer(data=posts)
        if post_make_serializer.is_valid():
            post_make_serializer.save()
            mongo = MongoDbManager
            mongo.connection()
            posts = mongo.title_search(title=request.POST.title)
            post_make_serializer = PostReadSerializer(data=posts)
            return JsonResponse(post_make_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(post_make_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def post_detail(request, id):
    mongo = MongoDbManager()
    mongo.connection()
    try:
        posts = mongo.post_read(id)
    except Post.DoesNotExist:
        return JsonResponse({'message': '블로그 id의 내용이 없습니다,'},
                            status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET': # post read detail
        post_read_serializer = PostReadSerializer(posts, many=True)
        return JsonResponse(post_read_serializer.data, safe=False)
    elif request.method == 'PUT': # post edit
        post_data = JSONParser().parse(request)
        post_make_serializer = PostMakeSerializer(posts, data=post_data)
        if post_make_serializer.is_valid(): #값이 확실하냐?
            post_make =  mongo.post_update(id, post_data)
            return JsonResponse(post_make)
        return JsonResponse(post_make_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        mongo.post_delete(id)
        return JsonResponse({'message': '블로그 내용이 삭제되었습니다.'},
                            status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def tags(request):
    mongo = MongoDbManager()
    mongo.connection()

    if request.method == 'GET':
        posts = mongo.tags_search(request.GET)
        return JsonResponse(posts, safe=False)

    return JsonResponse({'message': '잘못된 형식의 호출입니다.'},
            status=status.HTTP_400_BAD_REQUEST)
