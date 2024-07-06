from django.contrib import admin
from .models import BookModel,Review,Category,Borrow,CustomUser,Profile

# Register your models here.
admin.site.register(BookModel)
admin.site.register(Review)
admin.site.register(Borrow)
admin.site.register(Profile)
admin.site.register(CustomUser)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('name',)}
    list_display=['name','slug']

admin.site.register(Category,CategoryAdmin) 