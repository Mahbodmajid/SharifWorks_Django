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
    title = models.CharField(max_length=20, blank=True)
    skills = models.ManyToManyField(Skill, related_name='skills')
    bio = models.TextField(blank=True)
    homepage = models.URLField(blank=True)
    cv = models.FileField(upload_to='files/cvs', blank=True)
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
    company_name = models.CharField(max_length=20)
    company_disc = models.TextField()
    company_type = models.BooleanField()  # False: public       True: private
    # founded_date = models.DateField(blank=True)
    homepage = models.URLField(blank=True)
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


class Comment(models.Model):
    employer = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE)
    job_seeker = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE)
    description = models.TextField()
    rate = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)


class Choices:
    JOBTYPES = (
        ('F', 'Full-Time'),
        ('P', 'Part-Time'),
        ('I', 'Internship'),
        ('L', 'Freelancer')
    )

    JOBCATS = (
        ('WEB_DEV', 'Web_Developer'),
        ('MOBILE_DEV', 'Mobile_Developer'),
        ('APP_DESIGN', 'Application_Design'),
        ('PROJECT_MANAGEMENT', 'Project_Management'),
        ('MARKETING', 'Marketing'),
    )


DEFAULT_EMP_ID = 1


class Advertise(models.Model):
    employer = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE, default=DEFAULT_EMP_ID)
    title = models.CharField(max_length=100)
    deadline = models.DateField(null=True)
    type = models.CharField(max_length=1, choices=Choices.JOBTYPES)
    category = models.CharField(max_length=20, choices=Choices.JOBCATS, blank=True)
    city = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    skills = models.ManyToManyField(Skill, related_name='ad_skills')


class JobReq(models.Model):
    advertise = models.ForeignKey(Advertise, on_delete=models.CASCADE)
    job_seeker = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE)
    state = models.IntegerField(default=1)  # 1: applied         2: accepted        3: rejected
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)


