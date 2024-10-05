
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# # Подключение к Redis
# redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

class Filler(models.Model):
    DEFAULT_FILLER = 0
    DEFAULT_DRINK1 = 0
    DEFAULT_DRINK2 = False

    drink1 = models.IntegerField(default=0)
    drink2 = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    info = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # Проверка и обработка значений перед сохранением
        if self.drink1 == '':
            self.drink1 = 0
        if self.drink2 == '':
            self.drink2 = 0

        # Преобразование значений в целые числа
        self.drink1 = int(self.drink1)
        self.drink2 = int(self.drink2)

        super().save(*args, **kwargs)


class Robot(models.Model):
    DEFAULT_SPEED = 70
    DEFAULT_TIME_WAIT = 5
    DEFAULT_LASER_MODE = 2
    DEFAULT_AUTOVALUE = True
    DEFAULT_PRESENCE_CUP = True

    speed = models.IntegerField(default=DEFAULT_SPEED)
    time_wait = models.IntegerField(default=DEFAULT_TIME_WAIT)
    laser_mode = models.IntegerField(default=DEFAULT_LASER_MODE)
    autovalue = models.BooleanField(default=DEFAULT_AUTOVALUE)
    presence_cup = models.BooleanField(default=DEFAULT_PRESENCE_CUP)


    def reset_to_default(self): 
        self.speed = self.DEFAULT_SPEED
        self.time_wait = self.DEFAULT_TIME_WAIT
        self.laser_mode = self.DEFAULT_LASER_MODE
        self.autovalue = self.DEFAULT_AUTOVALUE
        self.presence_cup = self.DEFAULT_PRESENCE_CUP
        self.save()


class Control(models.Model):
    calibration = models.BooleanField(default=False)
    panel = models.BooleanField(default=False)
    motor = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        #get_control_from_redis()

    def __str__(self):
        return f"Control(calibration={self.calibration}, panel={self.panel}, motor={self.motor})"