from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Car, Book, BookReaderRelation


class BookReaderSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField()
    reader_name = serializers.CharField()

    class Meta:
        model = BookReaderRelation
        fields = ('id', 'book_title', 'reader_name', 'pages_read', 'info', 'bool', 'mark')


class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField()
    category = serializers.CharField()

    class Meta:
        model = Book
        fields = ('id', "title", "pages", "category", "author_name")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create(email=validated_data['email'], username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class CarSerializer(serializers.ModelSerializer):
    brutal = serializers.SerializerMethodField()

    def get_brutal(self, instance):
        if instance.color == 'black':
            return True
        return False

    class Meta:
        model = Car
        fields = ['id', 'make', 'model', 'year', 'color', 'owner', 'cat', 'brutal']

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.make = validated_data.get('make', instance.make)
        instance.model = validated_data.get('model', instance.model)
        instance.year = validated_data.get('year', instance.year)
        instance.color = validated_data.get('color', instance.color)
        instance.save()
        return instance

