from network.models import Post, User
from django.contrib import admin


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('poster', 'timestamp', 'content')


admin.site.register(User)
admin.site.register(Post, PostAdmin)
