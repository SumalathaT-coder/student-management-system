from django import forms
from .models import Student,Course,Profile


class StudentForm(forms.ModelForm): 
    
    def clean_marks(self):
        marks = self.cleaned_data["marks"]
        
        if marks < 0 or marks > 100:
            raise forms.ValidationError("Marks must be between 0 and 100.")

        return marks
    
    def clean_age(self):
        age = self.cleaned_data["age"]

        if age < 5 or age > 100:
           raise forms.ValidationError("Age must be between 5 and 100.")

        return age

#  def clean(self):
#      cleaned_data = super().clean()

#        courses = cleaned_data.get("courses")
#        marks = cleaned_data.get("marks")
#
#       if courses and marks is not None:
#            for course in courses:
#               if course.name == "DAA" and marks < 40:
#                   raise forms.ValidationError(
#                        "DAA students must have at least 40 marks."
#                    )

#        return cleaned_data

    class Meta:
        model = Student
        fields = ["name", "age", "email", "courses", "marks"]
        
        
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = "__all__"
        
        
        
class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ["phone_number", "address"]

        widgets = {
            "phone_number": forms.TextInput(
                attrs={
                    "placeholder": "Enter phone number"
                }
            ),
            "address": forms.TextInput(
                attrs={
                    "placeholder": "Enter address"
                }
            ),
        }