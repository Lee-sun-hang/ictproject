from django.db import models

# Create your models here.

class user(models.Model):
    user_id = models.AutoField(primary_key=True)
    admin_yn = models.CharField(max_length=1)
    name = models.CharField(max_length=10)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    update_date = models.DateTimeField(auto_now_add=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True)


class upload_file(models.Model):
    upload_file_id = models.AutoField(primary_key=True)
    rename = models.CharField(max_length=100)
    save_path = models.CharField(max_length=200)
    ori_name = models.CharField(max_length=100)
    size = models.CharField(max_length=100)
    state_code = models.CharField(max_length=100)
    update_date = models.DateTimeField(auto_now_add=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True)

class board(models.Model):
    board_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(user, on_delete=models.CASCADE)
    upload_file_id = models.ForeignKey(upload_file, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    cotent = models.CharField(max_length=2000)
    update_date = models.DateTimeField(auto_now_add=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True)


 # reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)