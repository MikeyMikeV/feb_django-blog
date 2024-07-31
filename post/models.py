from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to="images/post")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return f"{self.id} {self.title} {self.created_at}"


import os
from django.dispatch import receiver

@receiver(models.signals.post_delete, sender=Post)
def delete_media_file_post(sender, instance: Post, **kwargs):
    if instance.image and os.path.isfile(instance.image.path):
        print(f'File \'{instance.image}\' is deleted')
        os.remove(instance.image.path)


@receiver(models.signals.pre_save, sender=Post)
def delete_media_file_post(sender, instance: Post, **kwargs):
    try:
        old_post = Post.objects.get(pk=instance.pk)
        if old_post.image != instance.image:
            if instance.image and os.path.isfile(instance.image.path):
                print(f'File \'{instance.image}\' is deleted')
                os.remove(instance.image.path)
    except:
        print("Пост сохранен в первый раз")