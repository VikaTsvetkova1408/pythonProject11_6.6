from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.IntegerField(default=0)

    def update_rating(self):
        self.user_rating = 0
        for post in Post.objects.filter(author__user=self.user):
            self.user_rating += post.post_rating * 3
            for comment in Comment.objects.filter(post=post):
                self.user_rating += comment.comment_rating
        for comment in Comment.objects.filter(user=self.user):
            self.user_rating += comment.comment_rating
        self.save()

    def __str__(self):

        return f'{self.user.username}'

class Category(models.Model):
    name = models.CharField(unique=True, max_length=255)


class Post(models.Model):
    object = None
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.BooleanField(True == 'news', False == 'articles')
    datetime = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')

    def like(self, amount=1):
        self.articles_rating += amount
        self.save()

    def dislike(self):
        self.like(-1)


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=255)
    comment_rating = models.IntegerField(default=0)

    def update_rating(self):
        self.comment_rating = 0
        for post in Post.objects.filter(author__comment=self.comment):
            self.comment_rating += post.post_rating * 3
            for comment in Comment.objects.filter(post=post):
                self.comment_rating += comment.comment_rating
        for comment in Comment.objects.filter(comment=self.comment):
            self.comment_rating += comment.comment_rating
        self.save()

    def __str__(self):

        return f'{self.comment.comment}'


    def like(self, amount=1):
        self.articles_rating += amount
        self.save()

    def dislike(self):
        self.like(-1)
