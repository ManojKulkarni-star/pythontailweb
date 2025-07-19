from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Student

from django.contrib.auth.models import User
import random
import string
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

def dashboard(request):
    return render(request, 'dashboard.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('student_list')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')



@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def forgot_password(request):
    if request.method == "POST":
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

            user.set_password(temp_password)
            user.save()

            return render(request, 'forgot_password.html', {
                'message': f"Temporary password for '{username}': {temp_password}. Please login and change it immediately."
            })
        except User.DoesNotExist:
            return render(request, 'forgot_password.html', {
                'error': "Username not found. Please check and try again."
            })
    return render(request, 'forgot_password.html')


@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not request.user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
        elif new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
        else:
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Password changed successfully!')
            return redirect('dashboard')

    return render(request, 'change_password.html')

@login_required
def student_list(request):
    query = request.GET.get('q')
    if query:
        students = Student.objects.filter(
            Q(name__icontains=query) | Q(subject__icontains=query)
        )
    else:
        students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})


@login_required
def student(request):
    if request.method == 'POST':
        name = request.POST['name'].strip().capitalize()
        subject = request.POST['subject'].strip().capitalize()
        marks = int(request.POST['marks'])

        if Student.objects.filter(name__iexact=name, subject__iexact=subject).exists():
            return render(request, 'student.html', {
                'error': f"Student '{name}' with subject '{subject}' already exists!"
            })

        Student.objects.create(name=name, subject=subject, marks=marks)
        return redirect('student_list')

    return render(request, 'student.html')


@login_required
def edit(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        new_name = request.POST['name'].strip().capitalize()
        new_subject = request.POST['subject'].strip().capitalize()
        new_marks = int(request.POST['marks'])

        if Student.objects.exclude(id=student_id).filter(
            name__iexact=new_name, subject__iexact=new_subject
        ).exists():
            return render(request, 'edit.html', {
                'student': student,
                'error': f"Student '{new_name}' with subject '{new_subject}' already exists!"
            })

        student.name = new_name
        student.subject = new_subject
        student.marks = new_marks
        student.save()
        return redirect('student_list')

    return render(request, 'edit.html', {'student': student})


@login_required
def delete(request, student_id):
    if request.method == 'POST':
        student = get_object_or_404(Student, id=student_id)
        student.delete()
    return redirect('student_list')
