from django.contrib import admin
from .models import *
# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display=('name',
                  'author',
                  'isbn',
                  'category',)
                  
admin.site.register(Book,BookAdmin)

admin.site.register(Student)
admin.site.register(IssuedBook)