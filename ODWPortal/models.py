from django.db import models
from django.template.defaultfilters import truncatewords


class Language(models.Model):
    id = models.AutoField(primary_key=True)
    site_language = models.CharField(max_length=3, null=False, blank=False)
    afield = models.CharField(max_length=50, null=False)
    avalue = models.TextField(null=True)

    def truncate_value(self):
        return truncatewords(self.avalue, 30)


class Site(models.Model):
    id = models.AutoField(primary_key=True)
    site_name = models.CharField(max_length=256, null=False)
    site_url = models.CharField(max_length=256, null=False)
    date_added = models.DateTimeField(auto_now_add=True)
    language = models.CharField(max_length=3, null=False, blank=False)

    def __str__(self):
        return self.site_name


class SiteSetup(models.Model):
    id = models.AutoField(primary_key=True)
    site = models.ForeignKey(Site, null=False)
    afield = models.CharField(max_length=50, null=False)
    avalue = models.TextField(null=True)

    def truncate_value(self):
        return truncatewords(self.avalue, 30)


class SiteAlternateSearches(models.Model):
    id = models.AutoField(primary_key=True)
    site = models.ForeignKey(Site, null=False)
    alt_site_id = models.IntegerField(null=True, blank=True)
    site_order = models.FloatField(blank=True, null=True)
    site_relationship = models.IntegerField(null=True, blank=True)
    alt_site_url = models.CharField(null=True, blank=True, max_length=200)
    alt_site_label = models.CharField(null=True, blank=True, max_length=200)
    alt_site_syntax = models.CharField(null=True, blank=True, max_length=10)
