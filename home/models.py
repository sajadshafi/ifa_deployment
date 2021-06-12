from django.db import models

class AprDrugDescription(models.Model):
    id = models.AutoField(primary_key=True)
    apr_drg_description = models.TextField()
