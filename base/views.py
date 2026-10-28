import csv

from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView
)
from django.urls import reverse_lazy
from django.db.models import Q, Avg, Max, Min, Count

from .models import Student, Course
from .forms import StudentForm, CourseForm


class HomeView(View):

    def get(self, request):
        return render(request, "home.html")


class StudentListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView
):
    model = Student
    template_name = "view_students.html"
    context_object_name = "students"
    permission_required = "base.view_student"
    paginate_by = 5

    def get_queryset(self):

        if self.request.user.is_staff:

            queryset = Student.objects.all().order_by("id")

        elif self.request.user.groups.filter(
            name="Teacher"
        ).exists():

            queryset = Student.objects.filter(
                user=self.request.user
            ).order_by("id")

        else:

            queryset = Student.objects.none()

        search = self.request.GET.get("search")

        if search:

            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(email__icontains=search) |
                Q(courses__name__icontains=search)
            ).distinct()

        course = self.request.GET.get("course")

        if course:

            queryset = queryset.filter(
                courses__name=course
            )

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["courses"] = Course.objects.all()

        return context


class StudentDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView
):
    model = Student
    template_name = "student_detail.html"
    permission_required = "base.view_student"

    def get_queryset(self):

        if self.request.user.is_staff:

            return Student.objects.all()

        elif self.request.user.groups.filter(
            name="Teacher"
        ).exists():

            return Student.objects.filter(
                user=self.request.user
            )

        else:

            return Student.objects.none()


class StudentCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView
):
    model = Student
    form_class = StudentForm
    template_name = "add_student.html"
    permission_required = "base.add_student"
    success_url = reverse_lazy("view_students")

    def form_valid(self, form):

        form.instance.user = self.request.user

        response = super().form_valid(form)

        messages.success(
            self.request,
            f"Student {form.instance.name} added successfully!"
        )

        return response


class StudentUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView
):
    model = Student
    form_class = StudentForm
    template_name = "edit_student.html"
    permission_required = "base.change_student"
    success_url = reverse_lazy("view_students")

    def get_queryset(self):

        if self.request.user.is_staff:

            return Student.objects.all()

        elif self.request.user.groups.filter(
            name="Teacher"
        ).exists():

            return Student.objects.filter(
                user=self.request.user
            )

        else:

            return Student.objects.none()

    def form_valid(self, form):

        student_name = form.instance.name

        response = super().form_valid(form)

        messages.success(
            self.request,
            f"Student {student_name} updated successfully!"
        )

        return response


class StudentDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView
):
    model = Student
    template_name = "student_confirm_delete.html"
    permission_required = "base.delete_student"
    success_url = reverse_lazy("view_students")

    def get_queryset(self):

        if self.request.user.is_staff:

            return Student.objects.all()

        elif self.request.user.groups.filter(
            name="Teacher"
        ).exists():

            return Student.objects.filter(
                user=self.request.user
            )

        else:

            return Student.objects.none()

    def form_valid(self, form):

        student_name = self.get_object().name

        response = super().form_valid(form)

        messages.success(
            self.request,
            f"Student {student_name} deleted successfully!"
        )

        return response


class DashboardView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    View
):
    permission_required = "base.view_student"

    def get(self, request):

        if request.user.is_staff:

            students = Student.objects.all()

        elif request.user.groups.filter(
            name="Teacher"
        ).exists():

            students = Student.objects.filter(
                user=request.user
            )

        else:

            students = Student.objects.none()

        total_students = students.count()

        average_marks = students.aggregate(
            Avg("marks")
        )["marks__avg"]

        if average_marks is not None:

            average_marks = round(
                average_marks,
                2
            )

        highest_marks = students.aggregate(
            Max("marks")
        )["marks__max"]

        lowest_marks = students.aggregate(
            Min("marks")
        )["marks__min"]

        students_above_90 = students.filter(
            marks__gt=90
        ).count()

        students_below_60 = students.filter(
            marks__lt=60
        ).count()

        recent_students = students.order_by(
            "-created_at"
        )[:5]

        course_statistics = Course.objects.annotate(
            student_count=Count("student")
        )

        context = {
            "user": request.user,
            "total_students": total_students,
            "average_marks": average_marks,
            "highest_marks": highest_marks,
            "lowest_marks": lowest_marks,
            "students_above_90": students_above_90,
            "students_below_60": students_below_60,
            "recent_students": recent_students,
            "course_statistics": course_statistics,
        }

        return render(
            request,
            "dashboard.html",
            context
        )


class CourseListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView
):
    model = Course
    template_name = "course_list.html"
    context_object_name = "courses"
    permission_required = "base.view_course"

    def get_queryset(self):

        return Course.objects.prefetch_related(
            "student_set"
        ).annotate(
            student_count=Count("student")
        )


class CourseDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView
):
    model = Course
    template_name = "course_detail.html"
    context_object_name = "course"
    permission_required = "base.view_course"


class CourseUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView
):
    model = Course
    fields = ["name"]
    template_name = "edit_course.html"
    permission_required = "base.change_course"
    success_url = reverse_lazy("course_list")


class CourseDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView
):
    model = Course
    template_name = "course_confirm_delete.html"
    permission_required = "base.delete_course"
    success_url = reverse_lazy("course_list")


class CourseCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView
):
    model = Course
    form_class = CourseForm
    template_name = "add_course.html"
    permission_required = "base.add_course"
    success_url = reverse_lazy("course_list")


@login_required
def export_students_csv(request):

    # Only staff and teachers can export student data.
    is_teacher = request.user.groups.filter(
        name="Teacher"
    ).exists()

    if not request.user.is_staff and not is_teacher:
        return HttpResponseForbidden(
            "You don't have permission to export student data."
        )

    if request.user.is_staff:
        students = Student.objects.all().order_by("id")
    else:
        students = Student.objects.filter(
            user=request.user
        ).order_by("id")

    search = request.GET.get("search")

    if search:
        students = students.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(courses__name__icontains=search)
        ).distinct()

    course = request.GET.get("course")

    if course:
        students = students.filter(
            courses__name=course
        ).distinct()

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        'attachment; filename="students.csv"'
    )

    writer = csv.writer(response)

    writer.writerow([
        "Name",
        "Age",
        "Email",
        "Courses",
        "Marks",
        "Grade",
        "Result",
    ])

    for student in students:
        courses = ", ".join(
            course.name
            for course in student.courses.all()
        )

        writer.writerow([
            student.name,
            student.age,
            student.email,
            courses,
            student.marks,
            student.grade,
            student.result,
        ])

    return response



class ReportsView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    TemplateView
):
    template_name = "reports.html"
    permission_required = "base.view_student"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        if self.request.user.is_staff:

            students = Student.objects.all()

        elif self.request.user.groups.filter(
            name="Teacher"
        ).exists():

            students = Student.objects.filter(
                user=self.request.user
            )

        else:

            students = Student.objects.none()

        context["total_students"] = students.count()

        context["average_marks"] = students.aggregate(
            Avg("marks")
        )["marks__avg"]

        context["highest_marks"] = students.aggregate(
            Max("marks")
        )["marks__max"]

        context["lowest_marks"] = students.aggregate(
            Min("marks")
        )["marks__min"]

        passed_students = 0
        failed_students = 0

        for student in students:

            if student.result == "Pass":

                passed_students += 1

            else:

                failed_students += 1

        context["passed_students"] = passed_students
        context["failed_students"] = failed_students

        if context["total_students"] > 0:

            context["pass_percentage"] = (
                passed_students /
                context["total_students"]
            ) * 100

        else:

            context["pass_percentage"] = 0

        grade_counts = {
            "A+": 0,
            "A": 0,
            "B": 0,
            "C": 0,
            "D": 0,
            "E": 0,
            "F": 0,
        }

        for student in students:

            grade_counts[student.grade] += 1

        context["grade_counts"] = grade_counts

        context["grade_statistics"] = [
            ("A+", grade_counts["A+"]),
            ("A", grade_counts["A"]),
            ("B", grade_counts["B"]),
            ("C", grade_counts["C"]),
            ("D", grade_counts["D"]),
            ("E", grade_counts["E"]),
            ("F", grade_counts["F"]),
        ]

        return context