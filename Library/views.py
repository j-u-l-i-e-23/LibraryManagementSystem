from Library.forms import IssueBookForm
from . import forms, models
from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from .models import Book,Student,User,IssuedBook
from .forms import Bookform,Studentform,IssueBookForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import date


# Create your views here.

def index(request):
    return render(request, "index.html")
# def admin_navbar_fun(request):
#     return render(request,'admin_navbar.html')

# def basefun(request):
#     return render(request,'base.html')

@login_required(login_url = '/AdminLogin')
def bookfun(request):
    if request.method == "POST":
        c=Bookform(request.POST)
        if c.is_valid():
            c.save()
            messages.success(request,"Book Added Successfully")
        return redirect('AddBook')
    form1=Bookform()
    bk={'b':form1}
    
    return render(request,'add_book.html',bk)

@login_required(login_url = '/AdminLogin')
def viewbookfun(request):
    books = Book.objects.all()
    return render(request, "view_books.html", {'books':books})

def delete_book(request, myid):
    books = Book.objects.filter(id=myid)
    books.delete()
    return redirect("/ViewBook")


def student_registration(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        branch = request.POST['branch']
        classroom = request.POST['classroom']
        roll_no = request.POST['roll_no']
        image = request.FILES.get('image')
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            passnotmatch = True
            messages.success(request,"Password Mismatch")
            return render(request, "student_registration.html", {'passnotmatch':passnotmatch})
        user = User.objects.create_user(username=username, email=email, password=password,first_name=first_name, last_name=last_name)
        student = Student.objects.create(user=user, phone=phone, branch=branch, classroom=classroom,roll_no=roll_no, image=image)
        user.save()
        student.save()       
        alert=True
        messages.success(request,"Successfully Registered")
        return render(request, "student_registration.html",{'alert':alert})
    # stud={'stu':Student.objects.all()}
    return render(request,"student_registration.html")

@login_required(login_url = '/AdminLogin')
def view_students(request):
    students = Student.objects.all()
    return render(request, "view_students.html", {'students':students})

def delete_student(request, myid):
    students = Student.objects.filter(id=myid)
    students.delete()
    return redirect("/view_students")




# def admin_login_fun(request):
#     return render(request,'admin_login.html')



def student_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return HttpResponse("You are not a student!!")
            else:
                return redirect("/profile")
        else:
            messages.info(request,"Invalid Username or Password")
            return render(request,"student_login.html")
    return render(request,"student_login.html")


def admin_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return redirect("AddBook")
            else:
                return HttpResponse("You are not an admin.")
        else:
            alert = True
            messages.success(request,"Invalid Username or Password")
            return render(request, "admin_login.html", {'alert':alert})
    return render(request, "admin_login.html")


@login_required(login_url = '/student_login')
def edit_profile(request):
    student = Student.objects.get(user=request.user)
    if request.method == "POST":
        email = request.POST['email']
        phone = request.POST['phone']
        branch = request.POST['branch']
        classroom = request.POST['classroom']
        roll_no = request.POST['roll_no']

        student.user.email = email
        student.phone = phone
        student.branch = branch
        student.classroom = classroom
        student.roll_no = roll_no
        student.user.save()
        student.save()
        alert = True
        messages.info(request,"Profile Upadated Successfully")        
        return redirect("/edit_profile")
    return render(request, "edit_profile.html")

@login_required(login_url = '/student_login')
def profile(request):
    return render(request,"profile.html")


def change_password(request):
    if request.method == "POST":
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(current_password):
                u.set_password(new_password)
                u.save()
                # alert = True
                messages.success(request,"Password Updated Successfully")
                return render(request, "change_password.html")
            else:
                currpasswrong = True
                messages.info(request,"Current Password is Wrong")
                return render(request, "change_password.html")
        except:
            pass
    return render(request, "change_password.html")


@login_required(login_url = '/admin_login')
def issue_book(request):
    form = forms.IssueBookForm()
    if request.method == "POST":
        form = forms.IssueBookForm(request.POST)
        if form.is_valid():
            obj = models.IssuedBook()
            obj.student_id = request.POST['name2']
            obj.isbn = request.POST['isbn2']
            obj.save()
            messages.success(request,"Book Issued Successfully")
            alert = True
            return render(request, "issue_book.html", {'obj':obj, 'alert':alert})
    return render(request, "issue_book.html", {'form':form})


@login_required(login_url = '/student_login')
def student_issued_books(request):
    student = Student.objects.filter(user_id=request.user.id)
    issuedBooks = IssuedBook.objects.filter(student_id=student[0].user_id)
    li1 = []
    li2 = []

    for i in issuedBooks:
        books = Book.objects.filter(isbn=i.isbn)
        for book in books:
            t=(request.user.id, request.user.get_full_name, book.name,book.author)
            li1.append(t)

        days=(date.today()-i.issued_date)
        d=days.days
        fine=0
        if d>15:
            day=d-14
            fine=day*5
        t=(issuedBooks[0].issued_date, issuedBooks[0].expiry_date, fine)
        li2.append(t)
    return render(request,'student_issued_books.html',{'li1':li1, 'li2':li2})

@login_required(login_url = '/admin_login')
def view_issued_book(request):
    issuedBooks = IssuedBook.objects.all()
    details = []
    for i in issuedBooks:
        isb_id=i.id
        print(isb_id)
        days = (date.today()-i.issued_date)
        d=days.days
        fine=0
        if d>14:
            day=d-14
            fine=day*5
        # issue=list(models.IssuedBook.filter(IssuedBook.id))
        books = list(models.Book.objects.filter(isbn=i.isbn))
        students = list(models.Student.objects.filter(user=i.student_id))
        i=0
        for l in books:
            t=(students[i].user,
               students[i].user_id,
               books[i].name,
               books[i].isbn,
               issuedBooks[0].issued_date,
               issuedBooks[0].expiry_date,
               fine,
               isb_id)
            i=i+1
            details.append(t)
        # print("hii")
        print(issuedBooks[0].id)
    return render(request, "view_issued_book.html", {'details':details})


def delete_issue(request, myid):   
    issue = IssuedBook.objects.get(id=myid)
    issue.delete()
    return redirect("view_issued_book")






def Logout(request):
    logout(request)
    return redirect ("/")





