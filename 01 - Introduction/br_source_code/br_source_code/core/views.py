from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from customers.models import Customer 
from books.models import Book, BookTitle
from django.views.generic import TemplateView
from django.http import JsonResponse
from rentals.models import Rental
from publishers.models import Publisher
from rentals.choices import STATUS_CHOICES
from .forms import LoginForm, OTPForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .utils import send_otp, is_ajax
from datetime import datetime
import pyotp
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

def logout_view(request):
    logout(request)
    return redirect('login')

def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                send_otp(request)
                request.session['username'] = username
                print('ok, sending otp')
                return redirect('otp')
            else:
                messages.add_message(request, messages.ERROR, 'Invalid username or password')

    context = {
        'form': form
    }

    return render(request, 'login.html', context)


def otp_view(request):
    error_message = None
    form = OTPForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            otp = form.cleaned_data['otp']
            username = request.session['username']
            otp_secret_key = request.session['otp_secret_key']
            otp_valid_until = request.session['otp_valid_date']

            if otp_secret_key and otp_valid_until:
                valid_until = datetime.fromisoformat(otp_valid_until)
                if valid_until > datetime.now():
                    totp = pyotp.TOTP(otp_secret_key, interval=120)
                    if totp.verify(otp):
                        user = get_object_or_404(User, username=username)
                        login(request, user)
                        del request.session['otp_secret_key']
                        del request.session['otp_valid_date']
                        return redirect('home')
                    else:
                        error_message = 'Invalid one-time-password'
                else:
                    error_message = "One-time-password has expired"
            else:
                error_message = "Ups... something went wrong :("

        if error_message: messages.add_message(request, messages.ERROR, error_message)
    
    context = {'form': form}

    return render(request, 'otp.html', context)


@login_required
def change_theme(request):
    if 'is_dark_mode' in request.session:
        request.session['is_dark_mode'] = not request.session['is_dark_mode']
    else:
        request.session['is_dark_mode'] = True
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'


class AboutView(LoginRequiredMixin, TemplateView):
    template_name = 'about.html'


@login_required
def chart_data(request):

    if not is_ajax(request):
        return redirect('home')

    data = []
    # 1) book titles vs books (bar)
    all_books = len(Book.objects.all())
    all_book_titles = len(BookTitle.objects.all())
    data.append({
        'labels': ['books', 'book titles'],
        'data': [all_books, all_book_titles],
        'description': 'unique book titles vs books',
        'type': 'bar',
    })
    # 2) book title count by publisher (pie)
    titles_by_publisher = BookTitle.objects.values('publisher__name').annotate(Count('publisher__name'))
    publisher_names = [x['publisher__name'] for x in titles_by_publisher]
    publisher_names_count = [x['publisher__name__count'] for x in titles_by_publisher]
    data.append({
        'labels': publisher_names,
        'data': publisher_names_count,
        'description': 'book title count by publisher',
        'type': 'pie',
    })

    # 3) books by status (pie)
    book_by_status = Rental.objects.values('status').annotate(Count('book__title'))
    book_title_count = [x['book__title__count'] for x in book_by_status]
    status_keys = [x['status'] for x in book_by_status]
    status = [dict(STATUS_CHOICES)[key] for key in status_keys]
    data.append({
        'labels': status,
        'data': book_title_count,
        'description': 'book by status',
        'type': 'pie'
    })

    # 4) publishers vs customers (bar)
    customers = len(Customer.objects.all())
    publishers = len(Publisher.objects.all())
    data.append({
        'labels': ['customers', 'publishers'],
        'data': [customers, publishers],
        'description': 'customers vs publishers',
        'type' : 'bar'
    })

    print(data)

    return JsonResponse({'data': data})


# def home_view(request):
#     qs = Customer.objects.all()
#     # obj = Book.objects.get(id=1)
#     obj = BookTitle.objects.get(id=1)
#     books = obj.books
#     title = obj.title
#     print(books)
#     print(title)
#     context = {
#         'qs': qs, 
#         'obj': obj
#     }
#     return render(request, 'main.html', context)