# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Actorsinmovies(models.Model):
    aname = models.CharField(db_column='aName', primary_key=True, max_length=50)  # Field name made lowercase. The composite primary key (aName, mTitle) found, that is not supported. The first column is selected.
    mtitle = models.ForeignKey('Movies', models.DO_NOTHING, db_column='mTitle')  # Field name made lowercase.
    salary = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ActorsInMovies'
        unique_together = (('aname', 'mtitle'),)


class Movies(models.Model):
    title = models.CharField(primary_key=True, max_length=50)
    genre = models.CharField(max_length=50, blank=True, null=True)
    releasedate = models.DateField(db_column='releaseDate', blank=True, null=True)  # Field name made lowercase.
    budget = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Movies'


class Users(models.Model):
    uid = models.IntegerField(db_column='uID', primary_key=True)  # Field name made lowercase.
    country = models.CharField(max_length=50, blank=True, null=True)
    favactor = models.CharField(db_column='favActor', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Users'


class Watching(models.Model):
    uid = models.OneToOneField(Users, models.DO_NOTHING, db_column='uID', primary_key=True)  # Field name made lowercase. The composite primary key (uID, mTitle, wDate) found, that is not supported. The first column is selected.
    mtitle = models.ForeignKey(Movies, models.DO_NOTHING, db_column='mTitle')  # Field name made lowercase.
    wdate = models.DateField(db_column='wDate')  # Field name made lowercase.
    rating = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Watching'
        unique_together = (('uid', 'mtitle', 'wdate'),)
