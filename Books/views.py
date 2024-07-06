from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView
from users.models import UserBankAccount
from .forms import ReviewForm
from .models import BookModel, Borrow
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .models import BookModel, Review
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView
from django.views.generic.edit import FormView
from .forms import ChangeUserForm
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string


# Create your views here.
def send_transaction_email(user, amount, subject, template):
    message = render_to_string(
        template,
        {
            "user": user,
            "amount": amount,
        },
    )

    send_email = EmailMultiAlternatives(subject, "", to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()


def ReviewViewFunc(request, id):
    book = get_object_or_404(BookModel, pk=id)
    if request.method == "POST":
        form = ReviewForm(request, request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            user = request.user
            f.book = book
            f.user = user
            f.save()
            messages.success(request, f"Your Review Succesfully Submitted")
            return redirect("home")
    else:
        form = ReviewForm()
    return render(request, "./Books/review.html", {"form": form})


class BookDetailsView(DetailView):
    def get(self, request, id):
        book = get_object_or_404(BookModel, id=id)
        print(book.id)
        borrow_instance = Borrow.objects.filter(
            book=book, user=request.user, return_date__isnull=True
        ).first()
        context = {
            "book": book,
            "is_borrowed": borrow_instance is not None,
        }
        return render(request, "./Books/book_details.html", context)


@login_required
def BorrowBookView(request, id):
    book = get_object_or_404(BookModel, pk=id)

    try:
        requested_user = UserBankAccount.objects.get(user=request.user)
    except UserBankAccount.DoesNotExist:
        messages.error(
            request, "You need to create a bank account before borrowing books."
        )
        return redirect("registration")

    try:
        borrow = Borrow.objects.get(user=request.user, book=book)
    except Borrow.DoesNotExist:
        borrow = None

    if borrow is None:
        if requested_user.balance >= book.price:
            requested_user.balance -= book.price
            requested_user.save()
            Borrow.objects.create(user=request.user, book=book)
            messages.success(request, "You borrowed this book successfully.")
            send_transaction_email(
                request.user,
                requested_user.balance,
                "Borrow Message",
                "./Books/borrow_email.html",
            )
            return redirect("profile")
        else:
            messages.error(
                request,
                "You cannot borrow this book because your balance is less than the book price.",
            )
    else:
        messages.error(request, "This book is already borrowed.")

    return redirect("book_detail", id=id)


@login_required
def ReturnBook(request, id):
    book = get_object_or_404(BookModel, pk=id)
    borrow_instance = get_object_or_404(Borrow, book=book)

    if borrow_instance.user == request.user:
        usr = request.user
        usr.account.balance += book.price
        usr.account.save(update_fields=["balance"])

        borrow_instance.return_date = datetime.now()
        borrow_instance.save(update_fields=["return_date"])

        messages.success(request, "Book Returned successfully!!!")
        send_transaction_email(
            request.user,
            book.price,
            "Book Return Message",
            "Books/return_book_email.html",
        )

    return redirect("home")


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "./Books/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        borrowed_books = Borrow.objects.filter(user=self.request.user)
        context["borrowed_books"] = borrowed_books
        return context


@login_required
def submit_review(request, book_id):
    if request.method == "POST":
        book = get_object_or_404(BookModel, id=book_id)
        review_body = request.POST["review_body"]
        rating = request.POST["rating"]

        Review.objects.create(
            book=book, user=request.user, body=review_body, rating=rating
        )

        messages.success(request, "Review submitted successfully!!!")
        return redirect("home")

    return redirect("book_detail", book_id=book_id)


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ChangeUserForm
    template_name = "./Books/update_profile.html"
    success_url = reverse_lazy("home")

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Profile Update Successfully!!!")
        return super().form_valid(form)


class PassChangeView(LoginRequiredMixin, FormView):
    form_class = PasswordChangeForm
    template_name = "./Books/pass_change.html"
    success_url = reverse_lazy("home")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, "Password Updated Successfully!!!")
        return super().form_valid(form)


class DeleteBorrowedBookView(View):
    def get(self, request, book_id):
        book = get_object_or_404(Borrow, id=book_id, user=request.user)

        if book.return_date:
            book.delete()
            messages.success(request, "Returned books record has been deleted")
        else:
            messages.error(request, "Cannot delete a book without returned")

        return redirect("profile")
