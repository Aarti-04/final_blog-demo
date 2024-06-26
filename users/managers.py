from typing import Any
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.db.models import Q
# from .models import Category



class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)
# class CustomeUserMethods(models.Manager):
#     def first_user(self,id):
#        return super().get_queryset().filter(pk=id).first()
# class CustomTokenManager(models.Manager):
#     def check_token(self,access_token):
#         return super().get_queryset().filter(access_token=access_token).first()
#     def delete_token(self,token):
#         # print("in....")
#         print(token)
#         # return super().get_queryset().filter(access_token=token).first().delete()
#     def get_all(self):
#         return super().get_queryset().all()
class PostManager(models.Manager):
    def post_filter(self,search_by,order_by):
        return super().get_queryset().prefetch_related("post_comment__parent_comment").filter(Q(title__icontains=search_by) | Q(category__name__icontains=search_by)|Q(content__icontains=search_by)|Q(userid__email__icontains  =search_by)).order_by(order_by)
        
    # def get_post_and_related_comments(self):
    #    return super().get_queryset().prefetch_related("post_comment")
class CommentManager(models.Manager):
    def comment_filter(self,search_by,order_by):
        return super().get_queryset().filter(Q(comments__icontains=search_by)|Q(userid__email__icontains=search_by)|Q(postid__title__icontains=search_by)).order_by(order_by)

        