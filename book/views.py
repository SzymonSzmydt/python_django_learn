from django.views.generic import DetailView
from author.models import Author
from book.models import Book
from bookcopy.models import BookCopy
from genre.models import Genre
from django.views.generic import ListView
from django.db.models import Q


class BookListView(ListView):
    """
    Widok wyświetlający listę książek z obsługą paginacji
    oraz filtrowania po tytule, autorze lub gatunku.

    Funkcjonalności:
    - pobieranie książek wraz z autorem i gatunkiem,
    - wyszukiwanie książek na podstawie parametru `q`,
    - filtrowanie wyników według:
        * tytułu (`title`),
        * autora (`author`),
        * gatunku (`genre`),
    - paginacja wyników po 10 elementów na stronę,
    - przekazywanie listy autorów i gatunków do template.
    """

    model = Book
    template_name = "books/book_list.html"
    context_object_name = "books"
    paginate_by = 10

    def get_queryset(self):
        """
        Zwraca queryset książek z opcjonalnym filtrowaniem
        na podstawie parametrów GET.

        Parametry:
        - q: fraza wyszukiwania,
        - filter_by: pole używane do filtrowania
          (title, author, genre).

        Returns:
            QuerySet: przefiltrowana lista książek.
        """
        qs = (
            Book.objects
            .select_related("author", "genre")
        )

        q = self.request.GET.get("q")
        filter_by = self.request.GET.get('filter_by', 'title')

        if q:
            if filter_by == 'title':
                qs = qs.filter(Q(title__icontains=q))

            elif filter_by == 'author':
                qs = qs.filter(author__full_name__icontains=q)

            elif filter_by == 'genre':
                qs = qs.filter(genre__name__icontains=q)

        return qs

    def get_context_data(self, **kwargs):
        """
        Dodaje do kontekstu listę wszystkich autorów
        oraz gatunków dostępnych w systemie.

        Returns:
            dict: kontekst przekazywany do template.
        """
        context = super().get_context_data(**kwargs)
        context["authors"] = Author.objects.all()
        context["genres"] = Genre.objects.all()
        return context


class BookDetailView(DetailView):
    """
    Widok szczegółów pojedynczej książki.

    Funkcjonalności:
    - pobieranie danych książki wraz z autorem i gatunkiem,
    - pobieranie powiązanych egzemplarzy książki,
    - wyliczanie liczby dostępnych egzemplarzy książki.
    """

    model = Book
    template_name = "books/book_detail.html"
    context_object_name = "book"

    def get_queryset(self):
        """
        Zwraca queryset książek wraz z powiązanymi relacjami,
        aby ograniczyć liczbę zapytań do bazy danych.

        Returns:
            QuerySet: queryset książek z relacjami.
        """
        return (
            Book.objects
            .select_related("author", "genre")
            .prefetch_related("bookcopys")
        )

    def get_context_data(self, **kwargs):
        """
        Dodaje do kontekstu liczbę dostępnych egzemplarzy książki.

        Returns:
            dict: kontekst przekazywany do template.
        """
        context = super().get_context_data(**kwargs)

        book = self.object

        context["available_copies"] = len([
            copy for copy in book.bookcopys.all()
            if copy.status == BookCopy.Status.AVAILABLE
        ])

        return context