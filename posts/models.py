from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class Post(models.Model):
    title = models.CharField(max_length=300)
    url = models.URLField(blank=True, null=True)  # Optional URL
    text = models.TextField(blank=True)  # For text posts (no URL)
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    
    class Meta:
        ordering = ['-score', '-created_at']  # Default ordering by score, then time
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post_detail', args=[self.pk])
    
    @property
    def is_link_post(self):
        """Check if this is a link post (has URL) or text post"""
        return bool(self.url)
    
    @property
    def comment_count(self):
        return self.comments.count()

    @comment_count.setter
    def comment_count(self, value):
        pass


class Comment(models.Model):
    content = models.TextField()
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    
    class Meta:
        ordering = ['-score', 'created_at']
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
    
    @property
    def is_reply(self):
        """Check if this is a reply to another comment"""
        return bool(self.parent)
    
    def get_replies(self):
        """Get all direct replies to this comment"""
        return self.replies.all()


class Vote(models.Model):
    VOTE_CHOICES = [
        (1, 'Upvote'),
        # We only support upvotes for now, but this structure allows for downvotes later
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    vote_type = models.IntegerField(choices=VOTE_CHOICES, default=1)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        # Ensure a user can only vote once per post/comment
        unique_together = [
            ['user', 'post'],
            ['user', 'comment'],
        ]
    
    def __str__(self):
        target = self.post if self.post else self.comment
        return f"{self.user.username} voted on {target}"
    
    def clean(self):
        # Ensure vote is for either a post OR a comment, not both
        if self.post and self.comment:
            raise ValidationError("Vote cannot be for both post and comment")
        if not self.post and not self.comment:
            raise ValidationError("Vote must be for either a post or comment")


# Extend User model with additional fields
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    karma = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user.username}'s profile"
    
    def calculate_karma(self):
        """Calculate total karma from upvotes on user's posts and comments"""
        post_karma = Vote.objects.filter(post__author=self.user, vote_type=1).count()
        comment_karma = Vote.objects.filter(comment__author=self.user, vote_type=1).count()
        self.karma = post_karma + comment_karma
        self.save()
        return self.karma
