import odesk
from datetime import datetime
from django.contrib.auth.models import User
from django.db import models


class OdeskProfile(models.Model):
    user = models.OneToOneField(User, related_name='odesk_profile')
    # client.hr.get_user_me()
    reference = models.CharField(max_length=20, null=True, blank=True)
    odesk_id = models.CharField(max_length=30, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    timezone = models.CharField(max_length=255, null=True, blank=True)
    timezone_offset = models.IntegerField(null=True, blank=True)
    is_provider = models.BooleanField(blank=True)
    status = models.CharField(max_length=20, null=True, blank=True)
    # client.auth.get_info()
    portrait_50_img = models.URLField(null=True, blank=True)
    portrait_32_img = models.URLField(null=True, blank=True)
    portrait_100_img = models.URLField(null=True, blank=True)
    ref = models.CharField(max_length=10, null=True, blank=True)
    has_agency = models.BooleanField(blank=True)
    company_url = models.URLField(null=True, blank=True)
    capacity_provider = models.CharField(max_length=10, null=True, blank=True)
    capacity_buyer = models.CharField(max_length=10, null=True, blank=True)
    capacity_affiliate_manager = models.CharField(max_length=10, null=True, 
                                                    blank=True)

    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    profile_url = models.URLField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'odesk_profiles'


class Engagement(models.Model):
    #client.hr.get_engagements()
    profile = models.ForeignKey(OdeskProfile, related_name='engagements')
    buyer_team_id = models.CharField(max_length=50, null=True, blank=True)
    buyer_team_reference = models.CharField(max_length=50, null=True, 
                                                blank=True)
    created_time = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    dev_recno_ciphertext = models.CharField(max_length=50, null=True, 
                                                blank=True)
    engagement_end_date = models.CharField(max_length=50, null=True, 
                                                blank=True)
    engagement_job_type = models.CharField(max_length=30, null=True, 
                                                blank=True)
    engagement_start_date = models.CharField(max_length=50, null=True, 
                                                blank=True)
    engagement_title = models.CharField(max_length=255, null=True, 
                                                blank=True)
    hourly_charge_rate = models.DecimalField(max_digits=10, decimal_places=2,
                                                null=True, blank=True)
    hourly_pay_rate = models.DecimalField(max_digits=10, decimal_places=2,
                                            null=True, blank=True)
    is_paused = models.BooleanField(blank=True)
    is_trial_assignment = models.CharField(max_length=50, null=True, blank=True)
    job_title = models.CharField(max_length=255, null=True, blank=True)
    job_ref_ciphertext = models.CharField(max_length=50, null=True, 
                                                blank=True)
    offer_reference = models.CharField(max_length=50, null=True, blank=True)
    portrait_url = models.URLField(null=True, blank=True)
    provider_id = models.CharField(max_length=50, null=True, blank=True)
    provider_reference = models.CharField(max_length=50, null=True, blank=True)
    provider_team_id = models.CharField(max_length=50, null=True, blank=True)
    provider_team_reference = models.CharField(max_length=50, null=True, 
                                                blank=True)
    reference = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True)
    weekly_hours_limit = models.CharField(max_length=20, null=True, blank=True)
    weekly_salary_charge_amount = models.DecimalField(max_digits=10, 
                                                        decimal_places=2,
                                                        null=True, blank=True)
    weekly_salary_pay_amount = models.DecimalField(max_digits=10, 
                                                        decimal_places=2,
                                                        null=True, blank=True)
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2, 
                                            null=True, blank=True)


    class Meta:
        db_table = 'odesk_engagements'
        
