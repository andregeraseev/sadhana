from django.contrib import admin
from .models import Post, Post_Comment, Post_Category, Post_Tag

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'category', 'comments_count', 'tags_list')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'content']
    list_filter = ('pub_date', 'category', 'tags')
    date_hierarchy = 'pub_date'

class PostCommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'content', 'pub_date', 'author')
    search_fields = ['content', 'author']
    list_filter = ('pub_date', 'author')
    date_hierarchy = 'pub_date'

class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'count_posts')

class PostTagAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Post, PostAdmin)
admin.site.register(Post_Comment, PostCommentAdmin)
admin.site.register(Post_Category, PostCategoryAdmin)
admin.site.register(Post_Tag, PostTagAdmin)
