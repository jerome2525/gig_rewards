from djongo import models

class Axie(models.Model):
    axie_id = models.IntegerField()
    name = models.CharField(max_length=255)
    stage = models.IntegerField()
    current_price_usd = models.FloatField()
    class Meta:
        abstract = True

class BeastClass(Axie): pass
class AquaticClass(Axie): pass
class PlantClass(Axie): pass
class BirdClass(Axie): pass
class BugClass(Axie): pass
class ReptileClass(Axie): pass
class MechClass(Axie): pass
class DawnClass(Axie): pass
class DuskClass(Axie): pass
