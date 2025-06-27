from django import forms

class BulletinUploadForm(forms.Form):
    pdf = forms.FileField(label="Upload Bulletin PDF") 