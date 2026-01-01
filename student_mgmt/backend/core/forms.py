from django import forms
from .models import Student, Course, Enrollment

class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'

class StudentForm(BaseForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'student_id', 'email']

class CourseForm(BaseForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'teacher']

class EnrollmentForm(BaseForm):
    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'grade']
