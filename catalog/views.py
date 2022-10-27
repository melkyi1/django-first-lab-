from django.shortcuts import render
from django.views import generic

from .models import Book, Author, BookInstance, Genre
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from .forms import RenewBookForm

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author





def index(request):
    # Генерация "количеств" некоторых главных объектов
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Доступные книги (статус = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    return render(
        request,
        'index.html',
        context=
        {'num_books': num_books, 'num_instances': num_instances, 'num_instances_available':num_instances_available,'num_authors':num_authors,'num_visits': num_visits},)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 2


def get_context_data(self, **kwargs):
    # В первую очередь получаем базовую реализацию контекста
    context = super(BookListView, self).get_context_data(**kwargs)
    # Добавляем новую переменную к контексту и инициализируем её некоторым значением
    context['some_data'] = 'This is just some data'
    return context

    context_object_name = 'my_book_list'
    # ваше собственное имя переменной контекста в шаблоне
    queryset = Book.objects.filter(title__icontains='war')[:5]
    # Получение 5 книг, содержащих слово 'war' в заголовке
    template_name = 'books/my_arbitrary_template_name_list.html'


# Определение имени вашего шаблона и его расположения


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 2


def get_context_data(self, **kwargs):
    # В первую очередь получаем базовую реализацию контекста
    context = super(AuthorListView, self).get_context_data(**kwargs)
    # Добавляем новую переменную к контексту и инициализируем её некоторым значением
    context['some_data'] = 'This is just some data'
    return context

    context_object_name = 'my_book_list'
    # ваше собственное имя переменной контекста в шаблоне
    queryset = Author.objects.filter(title__icontains='war')[:5]


class AuthorDetailView(generic.DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10


def get_queryset(self):
    return
    BookInstance.objects.filter(borrower=self.request.user).filter(status__exact = 'o').order_by('due_back')


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_inst = get_object_or_404(BookInstance, pk=pk)
    if request.method == 'POST':
        form = RenewBookForm(request.POST)
        if form.is_valid():
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()
            return HttpResponseRedirect(reverse('all-borrowed'))
        else:
                proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
                form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})
                return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})

class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial={'date_of_death':'12/10/2016',}


class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')


# Create your views here.
