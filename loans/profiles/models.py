from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User)
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=15, null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    hometown = models.TextField(null=True, blank=True)
    locale = models.CharField(max_length=20, null=True, blank=True)
    relationship_status = models.CharField(max_length=30, null=True, 
                                                            blank=True)
    verified = models.BooleanField(default=False)
    significant_other = models.TextField(null=True, blank=True)
    work = models.TextField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)

    # friends count
    friends_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'profiles_profiles'


def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'facebook':
        try:
            profile = user.get_profile()
            if profile is None:
                profile = Profile(user_id=user.id)
        except Profile.DoesNotExist:
            profile = Profile(user_id=user.id)

        # birthday
        birthday = response.get('birthday')
        if birthday is not None:
            profile.birthday = datetime.strptime(birthday, '%m/%d/%Y')

        profile.gender = response.get('gender')
        profile.link = response.get('link')
        profile.hometown = response.get('hometown')
        profile.locale = response.get('locale')
        profile.relationship_status = response.get('relationship_status')
        profile.significant_other = response.get('significant_other')
        profile.verified = response.get('verified')
        profile.work = response.get('work')
        profile.save()
