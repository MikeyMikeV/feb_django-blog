from django.contrib import admin
from .models import Post,PostAtachment

admin.site.register(Post)
admin.site.register(PostAtachment)