import jwt
import requests
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from django.contrib.auth.models import User
from .models import VisitorsCount
from .serializers import UserCollections, UserCollectionsSerializer


from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import ensure_csrf_cookie
from movies_web.utils import generate_access_token


def movies_list(request):
    page = request.GET.get('page')
    if page is None:
        page = 1
    url = 'https://demo.credy.in/api/v1/maya/movies/?'+'page='+str(page)
    auth = ('iNd3jDMYRKsN1pjQPMRz2nrq7N99q4Tsp9EY9cM0',
            'Ne5DoTQt7p8qrgkPdtenTK8zd6MorcCR5vXZIJNfJwvfafZfcOs4reyasVYddTyXCz9hcL5FGGIVxw3q02ibnBLhblivqQTp4BIC93LZHj4OppuHQUzwugcYu7TIC5H1')
    response = requests.api.get(url, auth=auth, timeout=10)
    count = response.json()['count']
    next = response.json()['next']
    previous = response.json()['previous']
    data = [i for i in response.json()['results']]
    data = {
        'count': count,
        'next': next,
        'previous': previous,
        'data': data,
    }
    return data


def extract_token(token):
    payload = jwt.decode(token, None, None)
    userid = payload['user_id']
    user = User.objects.get(id=userid)
    data = {
            'access_token': token,
            'firstname': user.first_name,
            'email': user.email,
            'username': user.username,
            'id': user.id
    }
    return data


@api_view(['POST'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def login_view(request):
    user = get_user_model()
    username = request.data['username']
    password = request.data['password']
    response = Response()
    if (username is None) or (password is None):
        raise exceptions.AuthenticationFailed(
            'username and password required')

    user = User.objects.filter(username=username).first()
    if(user is None):
        raise exceptions.AuthenticationFailed('user not found')
    if (not user.check_password(password)):
        raise exceptions.AuthenticationFailed('wrong password')

    access_token = generate_access_token(user)
    response.data = {
        'access_token': access_token,
    }

    return response


@api_view(['GET'])
def collection_home(request):
    if 'HTTP_AUTHORIZATION' in request.META:
        access = request.META['HTTP_AUTHORIZATION']
        info = extract_token(access)
        data = movies_list(request)
    else:
        data = {
            'is_success': False,
            'message': 'unauthorized'
        }
    return JsonResponse(data)


def db_collection(id):
    collection = UserCollections.objects.filter(user_id=id)
    favourite_genres = UserCollections.objects.filter(user_id=id, favourite_genres=True)[:3]
    collection = UserCollectionsSerializer(collection, many=True).data
    favourite_genres = UserCollectionsSerializer(favourite_genres, many=True).data
    return collection, favourite_genres


@csrf_exempt
@api_view(['GET', 'DELETE', 'PUT', 'POST'])
def collection(request, uuid=None):
    if 'HTTP_AUTHORIZATION' in request.META:
        access = request.META['HTTP_AUTHORIZATION']
        info = extract_token(access)
    if request.method == 'POST':
        data = request.data
        movies = data['movies']
        title = data['title']
        description = data['description']

        if access:
            r = UserCollections.objects.create(user_id=info['id'], title=title, description=description, movies=movies)
            data = {
                'collection_uuid': r.uuid
            }
            return JsonResponse(data, status=status.HTTP_202_ACCEPTED)
    elif request.method == 'GET':
        if info['id']:
            if uuid:
                try:
                    collection = UserCollections.objects.get(user_id=info['id'], uuid=uuid)
                    data = {
                        'title': collection.title,
                        'description': collection.description,
                        'movies': collection.movies,
                    }
                except ObjectDoesNotExist:
                    data = {
                        'is_success': False,
                        'message': 'matching record not found'
                    }
                return JsonResponse(data, safe=False)
            else:
                result = db_collection(info['id'])
                data = {
                    'is_success': True,
                    'data': {
                        'collections': result[0],
                        'favourite_genres': result[1]
                    }
                }
            return JsonResponse(data, safe=True)
    elif request.method == 'PUT':
        data = request.data
        movies = data['movies']
        title = data['title']
        description = data['description']
        f = UserCollections.objects.get(uuid=uuid)
        f.title = title
        f.description = description
        f.movies = movies
        f.save()
        data = {
            'title': title,
            'description': description,
            'movies': movies,
        }
        return JsonResponse(data)
    elif request.method == 'DELETE':
        UserCollections.objects.filter(user_id=info['id'], uuid=uuid).delete()
        data = {
            'is_success': True,
            'message': 'collection deleted successfully',
        }
        return JsonResponse(data)


@api_view(['GET'])
def server_hit_count(request):
    if 'HTTP_AUTHORIZATION' in request.META:
        access = request.META['HTTP_AUTHORIZATION']
        info = extract_token(access)
        count = VisitorsCount.objects.get(id=1).count
        data = {
            "requests": count
        }
        return JsonResponse(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def server_hit_reset_count(request):
    if 'HTTP_AUTHORIZATION' in request.META:
        access = request.META['HTTP_AUTHORIZATION']
        info = extract_token(access)
        VisitorsCount.objects.get(id=1).delete()
        data = {
            "message": "request count reset successfully"
        }
        return JsonResponse(data, status=status.HTTP_200_OK)

