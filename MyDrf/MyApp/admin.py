from django.contrib import admin
from .models import Car, Category, Profile, Book, BookReaderRelation


class BRAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'reader', 'pages_read', 'info', 'bool', 'mark')
    fields = ( 'book', 'reader', 'pages_read', 'info', 'bool', 'mark')


admin.site.register(Car)
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Book)
admin.site.register(BookReaderRelation, BRAdmin)
