from allauth.account.forms import SignupForm
from django import forms
from .models import Profile


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=100, label="First Name")
    last_name = forms.CharField(max_length=100, label="Last Name")
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": "Email Address"}),
    )

    JOB_CHOICES = [
        ("", "Select your job role"),
        ("student", "Student"),
        ("developer", "Developer"),
        ("sysadmin", "System Administrator"),
        ("security", "Security Specialist"),
        ("manager", "IT Manager"),
        ("consultant", "Consultant"),
        ("other", "Other"),
    ]

    job_role = forms.ChoiceField(
        choices=JOB_CHOICES,
        required=True,
    )

    def save(self, request):
        user = super().save(request)  # This saves the user with default email handling
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        user.save()  # Save the user to update with first name, last name, and email

        # Now we save the job_role to the Profile model
        profile, created = Profile.objects.get_or_create(user=user)
        profile.job_role = self.cleaned_data["job_role"]
        profile.save()  # Save the profile with the job role

        return user
