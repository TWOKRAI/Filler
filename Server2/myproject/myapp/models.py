from django.db import models

class Settings(models.Model):
    drink1 = models.IntegerField(default=0)
    drink2 = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    todo1 = models.BooleanField(default=False)
    todo2 = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Settings(drink1={self.drink1}, drink2={self.drink2}, todo1={self.todo1}, todo2={self.todo2}, status={self.status})"
