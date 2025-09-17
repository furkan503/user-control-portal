from django.db import models

# Create your models here.


class Geo(models.Model):
    lat = models.CharField(max_length=1000)
    lng = models.CharField(max_length=1000)

class Address(models.Model):
    street = models.CharField(max_length=1000)
    suite = models.CharField(max_length=1000)
    city = models.CharField(max_length=1000)
    zipcode = models.CharField(max_length=1000, null=True, blank=True)
    geo = models.OneToOneField(Geo, on_delete=models.CASCADE, related_name='address' , null=True, blank=True)

class Company(models.Model):
    name = models.CharField(max_length=1000)
    catchPhrase = models.CharField(max_length=1000)
    bs = models.CharField(max_length=1000)

class User(models.Model):
    name = models.CharField(max_length=1000)
    username = models.CharField(max_length=1000, default='default')
    email = models.CharField(max_length=1000, default='default@example.com')
    website = models.CharField(max_length=1000)
    phone = models.CharField(max_length=1000)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, related_name='user', null=True, blank=True)
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name='user', null=True, blank=True)
    image_file = models.ImageField(upload_to='images/', blank=True, null=True)



class Todo(models.Model):
    user = models.ForeignKey(User, related_name='todos',
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    completed = models.BooleanField(default=False)


class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts',
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    body = models.TextField()


class Comment(models.Model):
    post = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    email = models.EmailField()
    body = models.TextField()
    image_file = models.ImageField(upload_to='images/',blank=True, null=True)




class Album(models.Model):
    user = models.ForeignKey(
        User, related_name='albums', on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)


class Photo(models.Model):
    album = models.ForeignKey(
        Album, related_name='photos', on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    url = models.CharField(max_length=1000)
    thumbnail_url = models.CharField(max_length=1000)
    image_file = models.ImageField(upload_to='images/',blank=True, null=True)

