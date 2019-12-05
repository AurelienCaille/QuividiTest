from django.shortcuts import render
from books.models import Book, Author, Notation
from django.views import generic
from django.db.models import Avg
from .forms import NoteBookForm, FilterBookForm
import logging
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.

logger = logging.getLogger(__name__)

class BookListView(generic.ListView):

    model = Book

    def get_queryset(self):

        author = self.request.GET.get('author', None)
        min_notation = self.request.GET.get('notation', 0)

        if author == None:
            return Book.objects.annotate(note=Avg('notation__note')).filter(note__gte=min_notation)

        books = Book.objects.filter(author = author).annotate(note=Avg('notation__note')).filter(note__gte=min_notation)

        return books



    def get_context_data(self, **kwargs):

        context = super(BookListView, self).get_context_data(**kwargs)
        context['author'] = self.request.GET.get('author', 'give-default-value')
        context['notation'] = self.request.GET.get('notation', 'give-default-value')

        return context

@login_required
def book_detail_view(request, pk):

        #get books
        try:
            book = Book.objects.get(pk=pk)
            notations = Notation.objects.filter(book=pk)
            notation = notations.aggregate(Avg('note'))

        except Book.DoesNotExist:
            raise Http404('Book does not exist')


        context = {
            'book' : book,
            'notation_list': notations,
            'notation' : notation,
        }

        #check form
        if request.method == 'POST':
            form = NoteBookForm(request.POST)
            if form.is_valid():
                
                #check if note already exist with this pair user/book
                if Notation.objects.filter(user_author=request.user, book=form.cleaned_data['book']).exists():
                    return HttpResponse('401 notation already exist', status=401)

                u = form.save()

                #update notation value
                notation = notations.aggregate(Avg('note'))
            
            else:
                logger.error('form invalid')
                logger.error(form.errors)

        else:
            context['form'] = NoteBookForm
        

        return render(request, 'books/book_detail.html', context=context)


def index(request):

    #Basics informations
    num_books = Book.objects.all().count()
    num_author = Author.objects.all().count()
    num_notation = Notation.objects.all().count()

    last_notations = Notation.objects.order_by('-date')[0:3]

    context = {
        'num_books' : num_books,
        'num_author' : num_author,
        'num_notations' : num_notation,
        'notation_list' : last_notations,
        'form' : FilterBookForm,
    }


    return render(request, 'index.html', context=context)