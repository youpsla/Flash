from django.db import models

class Magcli (models.Model):
    client = models.ForeignKey('clients.Customer', editable=False)
    magasin = models.ForeignKey('magasins.Magasin', editable=False)
    distance_home = models.IntegerField(null=True)
    distance_pro = models.IntegerField(null=True)
    match_category = models.NullBooleanField (null=True)
    
    class Meta:
        unique_together = ("client", "magasin")
    

    