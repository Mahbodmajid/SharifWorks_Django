from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _


class Skill(models.Model):
    name = models.CharField(max_length=20)


class JobSeekerProfile(models.Model):
    class Meta:
        verbose_name = _('Job Seeker Profile')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skills = models.ManyToManyField(Skill, related_name='tags')
    bio = models.TextField(blank=True)
    homepage = models.URLField(blank=True)
    cv = models.FileField(upload_to='files/cvs', blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            JobSeekerProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class EmployerProfile(models.Model):
    class Meta:
        verbose_name = _('Employer Profile')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=10)
    company_disc = models.TextField()
    company_type = models.BooleanField()  # False: public       True: private
    founded_date = models.DateField(blank=True)
    address = models.CharField(max_length=100)
    # TODO: not finished yet

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            JobSeekerProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Choices:
    JOBTYPES = (
        ('F', 'Full-Time'),
        ('P', 'Part-Time'),
        ('I', 'Internship'),
        ('L', 'Freelancer')
    )

    JOBCATS = (
        ('DEV', 'Developer'),
    )


class Advertise(models.Model):
    title = models.CharField(max_length=100)
    deadline = models.DateField(null=True)
    type = models.CharField(max_length=1, choices=Choices.JOBTYPES)
    category = models.CharField(max_length=3, choices=Choices.JOBCATS)
    address = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

