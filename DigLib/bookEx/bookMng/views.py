from django.shortcuts import render

from django.http import HttpResponse

from .models import MainMenu
from .forms import BookForm, CommentForm, RatingForm, ChatForm
from django.http import HttpResponseRedirect
from .models import Book, Comment, Rating, WishList, ChatMessage


from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required




class Register(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register-success')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)



def index(request):
    return render(request,
                  'bookMng/index.html',
                  {
                      'item_list': MainMenu.objects.all()
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def aboutus(request):
    return render(request,
                  'bookMng/aboutus.html',
                  {
                      'item_list': MainMenu.objects.all(),

                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def postbook(request):
    submitted = False
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            # form.save()
            book = form.save(commit=False)
            try:
                book.username = request.user
            except Exception:
                pass
            book.save()
            return HttpResponseRedirect('/postbook?submitted=True')
    else:
        form = BookForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request,
                  'bookMng/postbook.html',
                  {
                      'form': form,
                      'item_list': MainMenu.objects.all(),
                      'submitted': submitted,
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def displaybooks(request):
    books = Book.objects.all()
    for b in books:
        b.pic_path = b.picture.url[14:]

    return render(request,
                  'bookMng/displaybooks.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books,
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    book.pic_path = book.picture.url[14:]

    rating_form = RatingForm(request.POST or None)

    try:
        user_old_rating = Rating.objects.get(username=request.user)
    except Rating.DoesNotExist:
        user_old_rating = None

    if user_old_rating is not None:
        current_rating = str(user_old_rating.rating)
    else:
        current_rating = None

    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)

        if comment_form.is_valid():
            text = request.POST.get('text')
            if text is not None:
                new_comment = comment_form.save(commit=False)
                new_comment.book = book
                new_comment.username = request.user
                new_comment.text = text
                new_comment.save()
                comment_form = CommentForm()  # reset comment form
        else:
            comment_form = CommentForm()

        if rating_form.is_valid():
            # delete the user's old rating(s) if they exist
            if user_old_rating is not None:
                user_old_rating.delete()

            # save the current rating
            rating = request.POST.get('rating')
            current_rating = str(rating)

            new_rating = rating_form.save(commit=False)
            new_rating.book = book
            new_rating.username = request.user
            new_rating.rating = rating
            new_rating.save()
    else:
        comment_form = CommentForm()

    # calculate stats after submission of the new comments/ratings
    comments = Comment.objects.filter(book=book).order_by('-book_id')
    rating_list = Rating.objects.filter(book=book)

    # calculate the average rating for the book
    if len(rating_list) != 0:
        average_rating = round(sum(item.rating for item in rating_list) / len(rating_list), 1)
    else:
        average_rating = "N/A"

    rating_count = len(rating_list)

    return render(request,
                  'bookMng/book_detail.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'book': book,
                      'comments': comments,
                      'comment_form': comment_form,
                      'average_rating': average_rating,
                      'rating_count': rating_count,
                      'form': rating_form,
                      'rating': current_rating
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def mybooks(request):
    books = Book.objects.filter(username=request.user)
    for b in books:
        b.pic_path = b.picture.url[14:]

    return render(request,
                  'bookMng/mybooks.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books,
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def book_delete(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()
    print(book.name)
    return render(request,
                  'bookMng/delete_book.html',
                  {
                      'item_list': MainMenu.objects.all(),
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def searchbook(request):
    book_name = request.GET.get('search')
    books = None

    # only perform a search if there is a valid argument
    if book_name is not None:
        books = Book.objects.filter(name__icontains=book_name)
        for b in books:
            b.pic_path = b.picture.url[14:]

    return render(request,
                  "bookMng/search_results.html",
                  {
                      'item_list': MainMenu.objects.all(),
                      "books": books,
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def display_wishlist(request):
    books = []
    wished_books = WishList.objects.filter(username=request.user)
    for x in wished_books:
        print(x.book)
        books.append(Book.objects.filter(id=str(x.book))[0])

    for b in books:
        b.pic_path = b.picture.url[14:]

    return render(request,
                  'bookMng/wishlist.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books,
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def wishlist_add(request, book_id):
    new_book = Book.objects.get(id=book_id)
    msg = "The selected book has been added to your wishlist!"

    try:
        WishList.objects.get(book=book_id, username=request.user)
    except WishList.DoesNotExist:  # Only add the book if it's not already there
        WishList.objects.create(username=request.user, book=new_book)
    else:
        msg = "The selected book was already in your wishlist"

    return render(request,
                  'bookMng/wishlist_add.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'message': msg
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def wishlist_delete(request, book_id):
    wished_book = WishList.objects.get(book=book_id, username=request.user)
    if wished_book is not None:
        wished_book.delete()

    return render(request,
                  'bookMng/wishlist_delete.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'message': "The selected book has been removed from your wishlist!"
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def chat_room(request):
    messages = ChatMessage.objects.all()
    message_form = ChatForm()

    if request.method == 'POST':
        message_form = ChatForm(request.POST or None)

        if message_form.is_valid():
            text = request.POST.get('text')
            if text is not None:
                new_message = message_form.save(commit=False)
                new_message.username = request.user
                new_message.text = text
                new_message.save()
                message_form = ChatForm()

    return render(request,
                  'bookMng/chat.html',
                  {
                      'messages': messages,
                      'message_form': message_form
                  }
                  )
