from django.db import models

# Create your models here.

class Area(models.Model):
    areaid = models.AutoField(primary_key=True)
    countryid = models.PositiveIntegerField()
    chn_name = models.CharField(max_length=64)
    eng_name = models.CharField(max_length=64, blank=True, null=True)
    sort = models.PositiveIntegerField()

    class Meta:
        # managed = False
        db_table = 'area'
        app_label = 'running'



class Country(models.Model):
    countryid = models.AutoField(primary_key=True)
    chn_name = models.CharField(max_length=64)
    eng_name = models.CharField(max_length=64, blank=True, null=True)
    country_logo = models.CharField(max_length=120, blank=True, null=True)
    sort = models.PositiveIntegerField()

    class Meta:
        # managed = False
        db_table = 'country'
        app_label = 'running'


    def __str__(self):
        return self.chn_name if self.chn_name else ""


class Province(models.Model):
    provinceid = models.AutoField(primary_key=True)
    countryid = models.ForeignKey(Country, db_column='countryid', null=True, on_delete=models.SET_NULL)
    areaid = models.PositiveIntegerField(blank=True, null=True)
    chn_name = models.CharField(max_length=64)
    eng_name = models.CharField(max_length=64, blank=True, null=True)
    sort = models.PositiveIntegerField()

    class Meta:
        # managed = False
        db_table = 'province'
        app_label = 'running'

    def __str__(self):
        return self.chn_name if self.chn_name else ""

from smart_selects.db_fields import ChainedForeignKey


class City(models.Model):
    cityid = models.AutoField(primary_key=True)
    countryid = models.ForeignKey(Country, db_column='countryid', null=True, on_delete=models.SET_NULL)
    areaid = models.PositiveIntegerField(blank=True, null=True)
    # provinceid = models.ForeignKey(Province, db_column='provinceid', null=True, on_delete=models.SET_NULL)
    Provinceid = ChainedForeignKey(Province, chained_field="countryid", chained_model_field="countryid", show_all=False, auto_choose=True, sort=True, db_column="provinceid")

    chn_name = models.CharField(max_length=64)
    eng_name = models.CharField(max_length=64, blank=True, null=True)
    sort = models.PositiveIntegerField()

    class Meta:
        # managed = False
        db_table = 'city'
        app_label = 'running'

    def __str__(self):
        return self.chn_name if self.chn_name else self.eng_name if self.eng_name else ""
