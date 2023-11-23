from django.db import models
from django.contrib.auth.models import User



class Blogs(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    last_updated_at = models.DateTimeField(null=True, auto_now_add=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    targs = models.TextField(null=True, blank=True)


    class Meta:
        db_table = "Blogs"
        verbose_name = "Blog"

    def __str__(self):
        return self.title


class Likes(models.Model):
    liked_by = models.ForeignKey(User, on_delete=models.CASCADE) 
    blog = models.ForeignKey(Blogs, on_delete=models.CASCADE) 

