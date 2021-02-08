# from django.db import models
# from django.conf import settings
#
#
# class Profile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
#     company = models.CharField(max_length=100, null=True)
#
#     def __str__(self):
#         return 'Profile for user {}'.format(self.user.username)
