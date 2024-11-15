from allauth.account.forms import SignupForm
from yellow_hat.constants import JOB_CHOICES
from django import forms
from .models import Profile


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(
        max_length=100,
        label="First Name",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "First Name"}
        ),
    )
    last_name = forms.CharField(
        max_length=100,
        label="Last Name",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Last Name"}
        ),
    )
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Email Address"}
        ),
    )

    job_role = forms.ChoiceField(
        choices=JOB_CHOICES,
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        user.save()

        profile, created = Profile.objects.get_or_create(user=user)
        profile.job_role = self.cleaned_data["job_role"]
        profile.save()

        return user
