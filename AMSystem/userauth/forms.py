from django import forms

class UserAuthenticationForm(forms.Form):
    user_id = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_user_id(self):
        user_id = self.cleaned_data.get('user_id')
        return user_id

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return password
