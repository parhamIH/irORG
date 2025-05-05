# admin.py
from django.contrib import admin
from .models import *

class BaseCategorysAdmin(admin.ModelAdmin):
    list_display = ('name',)  # فرض کنید که فیلد name دارید

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)

class ColorAdmin(admin.ModelAdmin):
    list_display = ('name',)

# و سایر مدل‌ها به همین ترتیب...

# ثبت مدل‌ها با تنظیمات دلخواه
admin.site.register(BaseCategorys, BaseCategorysAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(BaseColor)
admin.site.register(Color, ColorAdmin)
admin.site.register(Size)
admin.site.register(Product)
admin.site.register(ProductPackage)
admin.site.register(Gallery)
admin.site.register(Comment)
