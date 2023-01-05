import os
import zipfile
import shutil
from django.conf import settings
# from django.utils import timezone
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
# from zipfile import ZipFile


from .models import ProjectNumber, Quotation, EmailData
from .forms import ProjectNumberForm, QuotationForm, AddEmailForm

def error_404(request):
	return render(request, 'quotation/404_error.html')

@login_required
def homeview(request):

	if request.user.acc_type == 'TP':
		return redirect(reverse('transpoter-home'))
	elif request.user.acc_type == 'AD':
		return redirect(reverse('general-home'))

	else:
		return redirect('error_404')



#--------------------------------------------------
## Delete Folders
def delete_folders(p_no):
	pass
#--------------------------------------------------


#--------------------------------------------------
## Comoress file and send Email

@login_required
def compress_file_send_email(p_no):

	# list the files in directory
	file_path = str(settings.BASE_DIR) + f'/quotation_files/{p_no}/'

	zipf_path = str(settings.BASE_DIR) + f'/Qzipfiles/'
	old_path = os.getcwd()

	os.chdir(zipf_path)

	zipf = zipfile.ZipFile(f"{p_no}.zip", "w", zipfile.ZIP_DEFLATED)

	for root, subdir, files in os.walk(file_path):
		for filename in files:
			zipf.write(os.path.abspath(os.path.join(root, filename)), arcname=filename)

	zipf.close()

	os.chdir(old_path)

	# print(f"Zip Operation Completed!")


#--------------------------------------------------


@login_required
def transpoterview(request):
	if request.user.acc_type != "TP":
		return redirect('home')

	user_model = get_user_model()

	try:
		# p_no = request.POST.get('project_no')
		send_user_pr_no = Quotation.objects.filter(user=request.user).all()
		project_no = ProjectNumber.objects.filter(project_status=False)
		transport_users_count = user_model.objects.filter(acc_type="TP").count()
	except:
		# p_no = None
		pass

	for p_no in project_no:
		# print("This is the valid project number.....")
		if p_no.p_count == transport_users_count or p_no.p_count >= transport_users_count:
			p_obj = ProjectNumber.objects.filter(project_no=p_no).get()
			p_obj.project_status = True
			p_obj.save()

			# compress data and send email
			compress_file_send_email(p_no)
			



	form = QuotationForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		
		try:
			p_no = request.POST.get('project_no')
			qf_path = str(settings.BASE_DIR) + f'/quotation_files/{p_no}/'
			up_file_names = [f.split('-_-')[0] for f in os.listdir(qf_path)]
		except:
			up_file_names = []
			
		if str(request.user) in up_file_names:
			msg = "Your Quotation File is Already Uploaded.."
			messages.add_message(request, messages.INFO, msg)

			return redirect('transpoter-home')
		
		obj = form.save(commit=False)
		obj.user = request.user
		obj.project_no = p_no
		
		p = ProjectNumber.objects.filter(project_no=p_no).get()
		p.p_count += 1

		obj.save()
		p.save()
		


		return redirect('transpoter-home')

	data = {'form': form, 'send_user_pr_no': send_user_pr_no}
	return render(request, 'quotation/transpoter_home.html', data)


@login_required
def generalview(request):
	if request.user.acc_type != "AD":
		return redirect('home')

	try:
		q_files = Quotation.objects.all()
		# project_no = [p_n for p_n in ProjectNumber.objects.filter(project_status=False)]
		project_no = ProjectNumber.objects.filter(project_status=False)
		e_data = [email.email for email in EmailData.objects.all()]

	except:
		q_files = None
		project_no = None
		e_data = None

	# transport_users_count = user_model.objects.filter(acc_type="TP").count()

	# for p_no in project_no:
	# 	if p_no.p_count == transport_users_count or p_no.p_count >= transport_users_count:
	# 		p_obj = ProjectNumber.objects.filter(project_no=p_no).get()
	# 		p_obj.project_status = True
	# 		p_obj.save()



	form = ProjectNumberForm(request.POST or None)

	if form.is_valid():
		obj = form.save(commit=False)
		obj.project_no = str(form.cleaned_data.get('project_no')).lower()
		obj.user = request.user

		obj.save()

		return redirect('general-home')

	data = {'form': form, 'q_files': q_files, 'project_no': project_no, }
	
	return render(request, 'quotation/general_home.html', data)

@login_required
def add_email(request):
	if request.user.acc_type != "AD":
		return redirect('home')

	try:
		emails = EmailData.objects.all()
	except:
		emails = None

	form = AddEmailForm(request.POST or None)

	if form.is_valid():
		form.save()

		return redirect('add-email')

	data = {'form': form, 'emails': emails}
	return render(request, 'quotation/add_email.html', data)

@login_required
def remove_email(request, id):
	email_data = EmailData.objects.get(pk=id)

	email_data.delete()

	return redirect('add-email')


