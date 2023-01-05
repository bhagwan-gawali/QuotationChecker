from django import forms

from .models import ProjectNumber, Quotation, EmailData

class ProjectNumberForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.fields['project_no'].widget.attrs.update({'class': 'form-control'})

	class Meta:
		model = ProjectNumber
		fields = ['project_no', ]

def get_choices():
		p_no = ProjectNumber.objects.filter(project_status=False).order_by('-id')
		return [(str(p).lower(), str(p)) for p in p_no]

class QuotationForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.fields['project_no'].widget.attrs.update({'class': 'form-select'})
		self.fields['company_name'].widget.attrs.update({'class': 'form-control'})
		self.fields['filedata'].widget.attrs.update({'class': 'form-control'})
		self.fields['project_no'].choices = get_choices()

	project_no = forms.ChoiceField()
	
	class Meta:
		model = Quotation
		fields = ['project_no', 'company_name', 'filedata', ]

class AddEmailForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.fields['email'].widget.attrs.update({'class': 'form-control'})

	class Meta:
		model = EmailData
		fields = ['email', ]