from django.db import models

# Create your models here.
class Animals(models.Model):
    id = models.AutoField(primary_key=True) # animalSeq
    status = models.DecimalField(max_digits=1, decimal_places=0) # 입양상태코드
    classification = models.DecimalField(max_digits=1, decimal_places=0) # 분류코드
    species = models.DecimalField(max_digits=3,decimal_places=0) # 품종
    is_mix = models.BooleanField() # 믹스여부
    gender = models.DecimalField(max_digits=1, decimal_places=0) # 성별코드
    age = models.TextField() # 나이
    weight = models.DecimalField(max_digits=3, decimal_places=1) # 몸무게
    haircolor = models.BinaryField(max_length=1) # 털색
    filepath = models.TextField() # 이미지경로
    gu = models.DecimalField(max_digits=1, decimal_places=0) # 발견 구
    locate = models.TextField() # 발견장소
    rescue_date = models.DateField() # 발견일

class Species(models.Model):
    id = models.AutoField(primary_key=True) # speciesSeq
    classification = models.DecimalField(max_digits=1, decimal_places=0) # 분류코드
    name = models.TextField() # 품종명
    name_kr = models.TextField() # 품종명(한글)