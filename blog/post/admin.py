from django.contrib import admin
from .models import Category,Post,PostAttachment,Comment


class PostAttachmentInline(admin.TabularInline):  
    model = PostAttachment
    extra = 1
    fields = ['photo', 'caption']  
    max_num = 10  

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name','category_slug']
    prepopulated_fields = {'category_slug': ('category_name',)}
    search_fields = ('category_name',)
    list_filter = ('category_name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title','author','publish','status','category']
    search_fields = ['title','text']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
    inlines = [PostAttachmentInline] 

    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author','post','created','active']
    list_filter = ['active','created','updated']
    search_fields = ['author','body']