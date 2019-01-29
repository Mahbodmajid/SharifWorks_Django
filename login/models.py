from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _


class Tag(models.Model):
    name = models.CharField(max_length=20)


class JobSeekerProfile(models.Model):
    class Meta:
        verbose_name = _('Profile')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # first_name = models.CharField(max_length=10, verbose_name='نام')
    email = models.EmailField(name='email', primary_key=True)
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    skills = models.ManyToManyField(Tag, related_name='tags')
    bio = models.TextField()
    joined_date = models.DateField(auto_now_add=True, null=True, blank=True)
    # homepage = models.URLField()
    cv = models.FileField(upload_to='files/cvs', null=True, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            JobSeekerProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(name='email', primary_key=True)
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    # TODO: not finished yet


