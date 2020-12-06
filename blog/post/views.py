from django.http.response import JsonResponse

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.parsers import JSONParser

from .serializers import PostMakeSerializer, PostReadSerializer
from .models import Post
from .mongo import search_post, update_post, delete_post


# post_make_* 은 포스트을 만들기 위한 최소의 직렬화 ('title', 'body', 'tags')
# post_read_* 은 포스트를 읽기 위한 모델의 전부다.. ('_id', 'title', 'body', 'tags','published_date')

# Create your views here.
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
            return JsonResponse(post_make_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(post_make_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def post_detail(request, id):
    try:
        posts = search_post(id=id)
    except Post.DoesNotExist:
        return JsonResponse({'message': '블로그 id의 내용이 없습니다,'},
                            status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET': # post read detail
        post_read_serializer = PostReadSerializer(posts, many=True)
        return JsonResponse(post_read_serializer.data, safe=False)
    elif request.method == 'PUT': # post edit
        post_data = JSONParser().parse(request)
        # post_data는 django_rest_framework에서 parse할때, tags가 list형식으로 불러와진다. json으로 수정
        post_make_serializer = PostMakeSerializer(posts, data=post_data)
        if post_make_serializer.is_valid():
            update_post(posts, post_data) #todo 이 부분 데이터 베이스느 입력은 내가 직접 만듬
            return JsonResponse(post_make_serializer.data)
        return JsonResponse(post_make_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        delete_post(id) #todo 이 부분 데이터베이스 제거도 직접 만들기
        return JsonResponse({'message': '블로그 내용이 삭제되었습니다.'},
                            status=status.HTTP_204_NO_CONTENT)
