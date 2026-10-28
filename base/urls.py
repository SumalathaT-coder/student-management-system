from django.urls import path
from . import views
from .views import DashboardView, ReportsView, CourseListView, CourseCreateView, CourseDetailView, CourseUpdateView, CourseDeleteView

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("view-students/", views.StudentListView.as_view(), name="view_students"),
    path("student/<int:pk>/", views.StudentDetailView.as_view(), name="student_detail"),
    path("add-student/", views.StudentCreateView.as_view(), name="add_student"),
    path("edit-student/<int:pk>/", views.StudentUpdateView.as_view(), name="edit_student"),
    path("delete-student/<int:pk>/", views.StudentDeleteView.as_view(), name="delete_student"),
    
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("reports/", ReportsView.as_view(), name="reports"),
    
    path("courses/", CourseListView.as_view(), name="course_list"),
    path("course/<int:pk>/", CourseDetailView.as_view(), name="course_detail"),
    path("course/<int:pk>/edit/", CourseUpdateView.as_view(), name="course_edit"),
    path("course/<int:pk>/delete/", CourseDeleteView.as_view(), name="course_delete"),
    path("add-course/", CourseCreateView.as_view(), name="add_course"),
    path("export-students-csv/", views.export_students_csv, name="export_students_csv"),
]