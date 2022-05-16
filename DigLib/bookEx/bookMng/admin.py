from django.contrib import admin

# Register your models here.

from .models import MainMenu
from .models import Book
from .models import Rating
from .models import Comment
from .models import WishList
from .models import ChatMessage

admin.site.register(MainMenu)
admin.site.register(Book)
admin.site.register(Rating)
admin.site.register(Comment)
admin.site.register(WishList)
admin.site.register(ChatMessage)
