from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='Profile')
    name = models.CharField(max_length=255, blank=False, null=False)
    dob = models.DateField(auto_now=True, blank=False, null=False)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return self.title


class Car(models.Model):
    make = models.CharField(max_length=255, blank=False, null=False)
    model = models.CharField(max_length=255, blank=False, null=False)
    year = models.IntegerField()
    color = models.CharField(max_length=50, blank=False, null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    cat = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return self.make


class Book(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pages = models.IntegerField(blank=False, null=False)
    cat = models.ForeignKey(Category, on_delete=models.PROTECT)
    reader = models.ManyToManyField(User, through='BookReaderRelation', related_name='reader')

    def __str__(self):
        return self.title


class BookReaderRelation(models.Model):
    MARKS = (
        (1, 'bad'),
        (2, 'ok'),
        (3, 'mid'),
        (4, 'good'),
        (5, 'incredible'),
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    reader = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    pages_read = models.IntegerField(blank=True, null=True)
    info = models.TextField(null=True, blank=True)
    bool = models.BooleanField(default=True)
    mark = models.PositiveIntegerField(choices=MARKS)

    def __str__(self):
        return self.book.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, name='Undefined')
