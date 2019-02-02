from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    is_jobseeker = models.BooleanField('jobseeker status', default=False)
    is_employer = models.BooleanField('employer status', default=False)


class Skill(models.Model):
    name = models.CharField(max_length=20)


class JobSeekerProfile(models.Model):
    class Meta:
        verbose_name = _('Job Seeker Profile')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="job_seeker_profile")
    skills = models.ManyToManyField(Skill, related_name='skills')
    bio = models.TextField(blank=True)
    homepage = models.URLField(blank=True)
    cv = models.FileField(upload_to='docs/cvs', blank=True)
    address = models.CharField(max_length=100, blank=True)

    # @receiver(post_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created and instance.is_jobseeker:
    #         JobSeekerProfile.objects.create(user=instance)
    #
    # @receiver(post_save, sender=User)
    # def update_user_profile(sender, instance, **kwargs):
    #     if instance.is_jobseeker:
    #         instance.job_seeker_profile.save()


class EmployerProfile(models.Model):
    class Meta:
        verbose_name = _('Employer Profile')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employer_profile")
    company_name = models.CharField(max_length=10)
    company_disc = models.TextField()
    company_type = models.BooleanField()  # False: public       True: private
    # founded_date = models.DateField(blank=True)
    address = models.CharField(max_length=100, blank=True)
    # TODO: not finished yet

    # @receiver(post_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created and instance.is_employer:
    #         JobSeekerProfile.objects.create(user=instance)
    #
    # @receiver(post_save, sender=User)
    # def update_user_profile(sender, instance, **kwargs):
    #     if instance.is_employer:
    #         instance.employer_profile.save()


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


DEFAULT_EMP_ID = 1


class Advertise(models.Model):
    employer = models.ForeignKey(User, on_delete=models.CASCADE, default=DEFAULT_EMP_ID)
    title = models.CharField(max_length=100)
    deadline = models.DateField(null=True)
    type = models.CharField(max_length=1, choices=Choices.JOBTYPES)
    category = models.CharField(max_length=3, choices=Choices.JOBCATS, blank=True)
    address = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

