from django.db import models
from django.contrib.auth.models import User
from categories.models import Categories
from django.forms import ModelForm
from django import forms
from geolocalisation import geocoding
from django.forms import widgets
from decimal import Decimal
# -*- coding: UTF-8 -*-
from django.db.models import signals
from magasins.signals import change_watcher
from django.db.models import get_model

class Magasin (models.Model):
    name = models.CharField(max_length=255, verbose_name = "Nom du magasin")
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    adresse = models.CharField(max_length=255)
    cp = models.IntegerField(max_length=5, verbose_name = "Code postal")
    ville = models.CharField(max_length=255)
    pays = models.CharField(max_length=128, default='France')
    category = models.ForeignKey(Categories, verbose_name = "Categorie")
    lat = models.DecimalField(max_digits=13, decimal_places=10)
    lng = models.DecimalField(max_digits=13, decimal_places=10)
    by = models.ForeignKey(User, editable=False)

    def magasin_evenements(self):
        Evenement = get_model('evenements','Evenement')
        return Evenement.objects.filter(magasin=self)
    

for signal in (signals.post_init, signals.post_save):
    signal.connect(change_watcher, sender = Magasin, dispatch_uid=signal)

class MagasinForm(ModelForm):
    class BlankIntField(forms.IntegerField):
        def clean(self, value):
            if not value:
                value = 0
            return Decimal(value)
    lat = BlankIntField(widget = widgets.HiddenInput())
    lng = BlankIntField(widget = widgets.HiddenInput())

    class Meta:
        model = Magasin
        exclude = ('by',)

    def clean(self):
        if self.cleaned_data.has_key('adresse') and self.cleaned_data.has_key('cp') and self.cleaned_data.has_key('ville'):
            lat, lng = geocoding (self.cleaned_data['adresse'], self.cleaned_data['cp'], self.cleaned_data['ville'])
            print "Lattitude %s - Longitude %s" % (lat, lng)
            self.cleaned_data['lat']=lat
            self.cleaned_data['lng']=lng
        else:
            pass
        return self.cleaned_data 


class MagasinOwnerProfile(models.Model):
    GENDER_CHOICES = (
            ('M', 'Monsieur'),
            ('MDE', 'Madame'),
            ('MELLE', 'Mademoiselle'),
        )
    user = models.ForeignKey(User, unique=True)
    genre = models.CharField(max_length=5, choices=GENDER_CHOICES)
    nom = models.CharField(max_length=100, blank=True)
    prenom = models.CharField(max_length=100, blank=True)
    telephone = models.CharField(max_length=14, blank=True)