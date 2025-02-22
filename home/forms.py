from django import forms
from .models import ContactMessage

class ContactMessageForm(forms.ModelForm):
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message', 'level', 'honeypot']

    def clean_honeypot(self):
        data = self.cleaned_data.get('honeypot')
        if data:
            raise forms.ValidationError("Bot detected.")
        return data
