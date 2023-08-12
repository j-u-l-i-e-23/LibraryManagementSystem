from django.urls import path
from .import views


urlpatterns=[
        #  path('',views.basefun,name='base'),
        #  path('admin_navbar',views.admin_navbar_fun,name='AdminNavbar'),
         path("", views.index, name="index"),
         path('AddBook/',views.bookfun,name='AddBook'),
         path('ViewBook/',views.viewbookfun,name='ViewBook'),
         path("view_students/", views.view_students, name="view_students"),
         path("delete_book/<int:myid>/", views.delete_book, name="delete_book"),
         path("StudentRegistration/", views.student_registration,name='StudentRegistration'),
         path("admin_login/", views.admin_login, name="admin_login"),
         path("student_login/", views.student_login, name="student_login"),
         path("profile/", views.profile, name="profile"),
         path("edit_profile/", views.edit_profile, name="edit_profile"),
        #  path("AdminLogin",views.admin_login_fun,name="AdminLogin"),
         path("change_password/", views.change_password, name="change_password"),

         path("issue_book/", views.issue_book, name="issue_book"),
         path("view_issued_book/", views.view_issued_book, name="view_issued_book"),
         path("delete_issue/<int:myid>/", views.delete_issue, name="delete_issue"),

         path("student_issued_books/", views.student_issued_books, name="student_issued_books"),
         path("logout/", views.Logout, name="logout"),
         path("delete_student/<int:myid>/", views.delete_student, name="delete_student"),
         
         


         ]   