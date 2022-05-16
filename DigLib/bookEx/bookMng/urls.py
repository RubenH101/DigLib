from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('book_detail/<int:book_id>', views.book_detail, name='book_detail'),
    path('postbook', views.postbook, name='postbook'),
    path('displaybooks', views.displaybooks, name='displaybooks'),
    path('mybooks', views.mybooks, name='mybooks'),
    path('book_delete/<int:book_id>', views.book_delete, name='book_delete'),
    path('searchbook', views.searchbook, name='searchbook'),
    path('aboutus', views.aboutus, name='aboutus'),
    path('wishlist', views.display_wishlist, name='display_wishlist'),
    path('wishlist_add/<int:book_id>', views.wishlist_add, name='wishlist_add'),
    path('wishlist_delete/<int:book_id>', views.wishlist_delete, name='wishlist_delete'),
    path('chat', views.chat_room, name='chat'),
]
