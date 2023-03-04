from django.contrib.auth.models import User
from django.db.models import F
from django.shortcuts import render, get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import CarSerializer, UserSerializer, BookSerializer, BookReaderSerializer
from .models import Car, Book, BookReaderRelation


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def home(request):
    tokens = get_tokens_for_user(get_object_or_404(User.objects.all(), pk=1))
    context = {
        "refresh": tokens['refresh'],
        'access': tokens['access']
    }
    return render(request, 'MyApp/home.html', context)


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class BookViewSet(ViewSet):
    queryset = Book.objects.all().annotate(author_name=F("author__username"), category=F("cat__title"))
    serializer_class = BookSerializer

    def list(self, request):
        serializer = BookSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        book = get_object_or_404(self.queryset, pk=pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)


class CarViewSet(ViewSet):
    queryset = Car.objects.all()
    permission_classes = []
    serializer_class = CarSerializer

    def list(self, request):
        serializer = CarSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        car = get_object_or_404(self.queryset, pk=pk)
        serializer = CarSerializer(car)
        return Response(serializer.data)

    def create(self, request):
        serializer = CarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        return Response("Error with your post request", serializer.errors)

    def partial_update(self, request, pk=None):
        car = get_object_or_404(self.queryset, pk=pk)
        serializer = CarSerializer(car, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, pk, format=None):
        item = get_object_or_404(Car.objects.all(), pk=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookReaderViewSet(ViewSet):
    queryset = BookReaderRelation.objects.all().annotate(reader_name=F('reader__username'), book_title=F('book__title'))
    serializer_class = BookReaderSerializer
    model = BookSerializer

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        obj = get_object_or_404(self.model)
        serializer = self.serializer_class(obj)
        return Response(serializer.data)

