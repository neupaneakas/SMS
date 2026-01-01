from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Student, Course, Enrollment
from .forms import StudentForm, CourseForm, EnrollmentForm

# Role decorators
def admin_required(view_func):
    return user_passes_test(lambda u: u.role=='admin', login_url='dashboard')(view_func)

def teacher_required(view_func):
    return user_passes_test(lambda u: u.role=='teacher', login_url='dashboard')(view_func)

# Auth views
def login_view(request):
    error = None
    if request.method=="POST":
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            error = "Invalid credentials"
    return render(request, "core/login.html", {"error": error})

def logout_view(request):
    logout(request)
    return redirect('login')

# Dashboard
@login_required
def dashboard_view(request):
    total_students = Student.objects.count()
    total_courses = Course.objects.count()
    total_enrollments = Enrollment.objects.count()
    return render(request, "core/dashboard.html", {
        "total_students": total_students,
        "total_courses": total_courses,
        "total_enrollments": total_enrollments
    })

# Students
@login_required
def students_view(request):
    q = request.GET.get('q','')
    students = Student.objects.filter(first_name__icontains=q) if q else Student.objects.all()
    return render(request, "core/students.html", {"students": students})

@admin_required
@login_required
def student_create(request):
    form = StudentForm(request.POST or None)
    if request.method=="POST" and form.is_valid():
        form.save()
        return redirect('students')
    return render(request, "core/student_form.html", {"form": form, "action":"Create"})

@admin_required
@login_required
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, instance=student)
    if request.method=="POST" and form.is_valid():
        form.save()
        return redirect('students')
    return render(request, "core/student_form.html", {"form": form, "action":"Update"})

@admin_required
@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method=="POST":
        student.delete()
        return redirect('students')
    return render(request, "core/student_delete.html", {"student": student})

# Courses (similar CRUD)
@login_required
def courses_view(request):
    q = request.GET.get('q','')
    courses = Course.objects.filter(name__icontains=q) if q else Course.objects.all()
    return render(request, "core/courses.html", {"courses": courses})

@admin_required
@login_required
def course_create(request):
    form = CourseForm(request.POST or None)
    if request.method=="POST" and form.is_valid():
        form.save()
        return redirect('courses')
    return render(request, "core/course_form.html", {"form": form, "action":"Create"})

@admin_required
@login_required
def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk)
    form = CourseForm(request.POST or None, instance=course)
    if request.method=="POST" and form.is_valid():
        form.save()
        return redirect('courses')
    return render(request, "core/course_form.html", {"form": form, "action":"Update"})

@admin_required
@login_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method=="POST":
        course.delete()
        return redirect('courses')
    return render(request, "core/course_delete.html", {"course": course})

# Enrollment / Grade assignment
@login_required
def enrollments_view(request):
    q = request.GET.get('q','')
    enrollments = Enrollment.objects.filter(student__first_name__icontains=q) if q else Enrollment.objects.all()
    return render(request, "core/enrollments.html", {"enrollments": enrollments})

@admin_required
@login_required
def enrollment_create(request):
    form = EnrollmentForm(request.POST or None)
    if request.method=="POST" and form.is_valid():
        form.save()
        return redirect('enrollments')
    return render(request, "core/enrollment_form.html", {"form": form, "action":"Enroll / Assign Grade"})
