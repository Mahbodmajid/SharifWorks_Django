# Generated by Django 2.1.5 on 2019-02-06 02:18

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_jobseeker', models.BooleanField(default=False, verbose_name='jobseeker status')),
                ('is_employer', models.BooleanField(default=False, verbose_name='employer status')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Advertise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('deadline', models.DateField(null=True)),
                ('type', models.CharField(choices=[('F', 'Full-Time'), ('P', 'Part-Time'), ('I', 'Internship'), ('L', 'Freelancer')], max_length=1)),
                ('category', models.CharField(blank=True, choices=[('WEB_DEV', 'Web_Developer'), ('MOBILE_DEV', 'Mobile_Developer'), ('APP_DESIGN', 'Application_Design'), ('PROJECT_MANAGEMENT', 'Project_Management'), ('MARKETING', 'Marketing')], max_length=20)),
                ('city', models.CharField(blank=True, max_length=50)),
                ('address', models.CharField(blank=True, max_length=100)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('rate', models.IntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmployerProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=10)),
                ('company_disc', models.TextField()),
                ('company_type', models.BooleanField()),
                ('homepage', models.URLField(blank=True)),
                ('address', models.CharField(blank=True, max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employer_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Employer Profile',
            },
        ),
        migrations.CreateModel(
            name='JobReq',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.IntegerField(default=1)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('deadline', models.DateTimeField(blank=True, null=True)),
                ('advertise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.Advertise')),
            ],
        ),
        migrations.CreateModel(
            name='JobSeekerProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=20)),
                ('bio', models.TextField(blank=True)),
                ('homepage', models.URLField(blank=True)),
                ('cv', models.FileField(blank=True, upload_to='files/cvs')),
                ('address', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'verbose_name': 'Job Seeker Profile',
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='jobseekerprofile',
            name='skills',
            field=models.ManyToManyField(related_name='skills', to='login.Skill'),
        ),
        migrations.AddField(
            model_name='jobseekerprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='job_seeker_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='jobreq',
            name='job_seeker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.JobSeekerProfile'),
        ),
        migrations.AddField(
            model_name='comment',
            name='employer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.EmployerProfile'),
        ),
        migrations.AddField(
            model_name='comment',
            name='job_seeker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.JobSeekerProfile'),
        ),
        migrations.AddField(
            model_name='advertise',
            name='employer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='login.EmployerProfile'),
        ),
        migrations.AddField(
            model_name='advertise',
            name='skills',
            field=models.ManyToManyField(related_name='ad_skills', to='login.Skill'),
        ),
    ]
