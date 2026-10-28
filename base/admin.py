from django.contrib import admin
from .models import Student, Profile, Course


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "age",
        "email",
        "display_courses",
        "marks",
        "created_at",
        "user",
    )

    search_fields = (
        "name",
        "email",
        "courses__name",
    )

    list_filter = ("courses",)

    ordering = ("name",)

    def display_courses(self, obj):
        return ", ".join(
            course.name for course in obj.courses.all()
        )

    display_courses.short_description = "Courses"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "phone_number",
        "address",
    )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    list_display = ("name",)

    search_fields = ("name",)