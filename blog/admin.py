from django.contrib import admin

# Register your models here.

from .models import BlogAuthor, Blog, BlogComment


admin.site.register(BlogAuthor)
admin.site.register(BlogComment)


#comment stuff here
class BlogCommentsInline(admin.TabularInline):
    model = BlogComment
    max_num=0


#blog stuff here
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'post_date')
    inlines = [BlogCommentsInline]