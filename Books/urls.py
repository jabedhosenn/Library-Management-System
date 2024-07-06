from django.urls import path
from . import views

urlpatterns = [
    path('review/<int:id>/',views.ReviewViewFunc,name='review'),
    path('details/<int:id>/',views.BookDetailsView.as_view(),name='book_details'),
    path('borrow_book/<int:id>/',views.BorrowBookView,name='borrow_book'),
    path('return_book/<int:id>/',views.ReturnBook,name='return_book'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('book/<int:book_id>/review/', views.submit_review, name='submit_review'),
    path('edit_profile/', views.EditProfileView.as_view(), name='edit_profile'),
    path('pass_change/', views.PassChangeView.as_view(), name='pass_change'),
    path('delete_borrowed_book/<int:book_id>/', views.DeleteBorrowedBookView.as_view(), name='delete_borrowed_book'),
]