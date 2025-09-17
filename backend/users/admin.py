from django.contrib import admin
from users.models import User, Todo, Post, Comment, Album, Photo, Company, Address, Geo




# Register your models here.

admin.site.register(User)
admin.site.register(Todo)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Album)
admin.site.register(Photo)
admin.site.register(Address)
admin.site.register(Company)
admin.site.register(Geo)

# admin.site.register(CustomUser, UserAdmin)



