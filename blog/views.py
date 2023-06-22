import uuid

import jwt
from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpResponse
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Users, BlogPost
from .serializers import UserSerializer, BlogPostSerializer


# def hello(request):
#     print('hello executed')
#     return HttpResponse('<H1>hello</H!>')


@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        password = request.data.get('password')
        user = serializer.save(password=make_password(password))  # Hash the password
        if user:
            username = user.username
            return Response({'message': 'Successfully registered!', 'username': username},
                            status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


secret_key = "your_secret_key"  # Replace with your actual secret key


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    try:
        # Find the user based on the username
        user = Users.objects.get(username=username)

        # Check if the provided password matches the encoded password
        if check_password(password, user.password):
            # Generate JWT token
            payload = {
                'user_id': user.id,
                'username': user.username
            }
            jwt_token = jwt.encode(payload, secret_key, algorithm='HS256')

            # Return the JWT token and username in the response
            response_data = {
                'token': jwt_token,
                'username': user.username
            }
            return Response(response_data)
        else:
            return Response({'error': 'Invalid username or password'}, status=401)

    except Users.DoesNotExist:
        return Response({'error': 'Invalid username or password'}, status=401)


@api_view(['GET'])
def protected_resource(request):
    token = request.headers.get('Authorization')

    if not token:
        return HttpResponse('Authorization token not provided', status=401)

    try:
        if secret_key is None:
            return HttpResponse('Access denied. Invalid secret key.', status=401)

        # Decode the JWT token using the secret key
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        user_id = payload.get('user_id')
        username = payload.get('username')

        # Check if the user is authorized (you can implement custom authorization logic here)
        if user_id and username:
            # Return the protected resource
            return HttpResponse('Access granted! Welcome, {}.'.format(username))

    except jwt.ExpiredSignatureError:
        return HttpResponse('Token has expired', status=401)
    except jwt.InvalidTokenError:
        return HttpResponse('Invalid token', status=401)

    return HttpResponse('Access denied', status=401)


class BlogPostFunction(APIView):
    # @staticmethod
    def post(self, request):
        token = request.headers.get('Authorization')

        if not token:
            return Response('Authorization token not provided', status=status.HTTP_401_UNAUTHORIZED)

        try:
            # secret_key = "your_secret_key"  # Replace with your actual secret key
            if secret_key is None:
                return Response('Access denied. Invalid secret key.', status=status.HTTP_401_UNAUTHORIZED)

            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            username = payload.get('username')

            if username:
                # Authentication successful, continue with the logic
                blogpost_serializer = BlogPostSerializer(data=request.data.get('blogposts'), many=True)

                if blogpost_serializer.is_valid():
                    try:
                        user = Users.objects.get(username=username)
                    except Users.DoesNotExist:
                        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

                    for blogpost_data in blogpost_serializer.validated_data:
                        BlogPost.objects.create(author=user, **blogpost_data)

                    return Response(blogpost_serializer.data, status=status.HTTP_201_CREATED)

                return Response(blogpost_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except jwt.ExpiredSignatureError:
            return Response('Token has expired', status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response('Invalid token', status=status.HTTP_401_UNAUTHORIZED)

        return Response('Access denied', status=status.HTTP_401_UNAUTHORIZED)


class BlogPostGetAll(APIView):
    # @staticmethod
    def get(self, request):
        token = request.headers.get('Authorization')

        if not token:
            return Response('Authorization token not provided', status=status.HTTP_401_UNAUTHORIZED)

        try:
            # secret_key = "your_secret_key"  # Replace with your actual secret key
            if secret_key is None:
                return Response('Access denied. Invalid secret key.', status=status.HTTP_401_UNAUTHORIZED)

            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            username = payload.get('username')

            if username:
                # Authentication successful, continue with fetching the blog posts
                blogposts = BlogPost.objects.all()
                serializer = BlogPostSerializer(blogposts, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError:
            return Response('Token has expired', status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response('Invalid token', status=status.HTTP_401_UNAUTHORIZED)

        return Response('Access denied', status=status.HTTP_401_UNAUTHORIZED)


class BlogPostUpdate(APIView):
    # @staticmethod
    def put(self, request, pk):
        token = request.headers.get('Authorization')

        if not token:
            return Response('Authorization token not provided', status=status.HTTP_401_UNAUTHORIZED)

        try:
            # secret_key = "your_secret_key"  # Replace with your actual secret key
            if secret_key is None:
                return Response('Access denied. Invalid secret key.', status=status.HTTP_401_UNAUTHORIZED)

            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            username = payload.get('username')

            if username:
                # Authentication successful, continue with updating the blog post
                try:
                    blogpost = BlogPost.objects.get(pk=pk)
                except BlogPost.DoesNotExist:
                    return Response({"error": "Blog post not found"}, status=status.HTTP_404_NOT_FOUND)

                serializer = BlogPostSerializer(blogpost, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except jwt.ExpiredSignatureError:
            return Response('Token has expired', status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response('Invalid token', status=status.HTTP_401_UNAUTHORIZED)

        return Response('Access denied', status=status.HTTP_401_UNAUTHORIZED)
