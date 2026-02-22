from django.db import models
from accounts.models import StudentProfile

class Post(models.Model):
    author = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(StudentProfile, related_name='liked_posts', blank=True)

    def __str__(self):
        return f"Post by {self.author.user.username} at {self.created_at}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.user.username} on {self.post.id}"
