import os
from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model

def upload_to(instance, filename):
	now = timezone.now()
	base, extension = os.path.splitext(filename)
	c_name = instance.company_name.replace(" ", "_")

	return f"quotation_files/{instance.project_no}/{instance.user}-_-{c_name}{extension}"

class ProjectNumber(models.Model):
	user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
	project_no = models.CharField(max_length=200, )
	project_status = models.BooleanField(default=False)
	create_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	p_count = models.PositiveIntegerField(default=0)

	def __str__(self):
		return self.project_no

class Quotation(models.Model):
	project_no = models.CharField(max_length=200, )
	company_name = models.CharField(max_length=200, )
	created_at = models.DateTimeField(auto_now_add=True)
	update_at = models.DateTimeField(auto_now=True)
	filedata = models.FileField(upload_to=upload_to)
	user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

	def __str(self):
		return self.company_name

class EmailData(models.Model):
	email = models.EmailField()


	def __str__(self):
		return self.email



