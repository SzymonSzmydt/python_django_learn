import random
import uuid
from django.core.management.base import BaseCommand
from faker import Faker
from author.models import Author
from book.models import Book
from bookcopy.models import BookCopy
from genre.models import Genre

AUTHOR_QTY = 10
BOOK_QTY = 50

GENRES = [
    "Fantastyka","Science Fiction","Horror","Thriller","Romans","Przygodowa","Kryminał","Biografia","Dramat","Poezja","Historyczna","Literatura młodzieżowa","Literatura dziecięca","Tajemnica"
]

class Command(BaseCommand):
    help = 'Seeds the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        fake = Faker('pl_PL')


        genres = []
        for name in GENRES:
            genre_obj, _ = Genre.objects.get_or_create(name=name)
            genres.append(genre_obj)

        self.stdout.write(self.style.SUCCESS(f'{len(genres)} genres created.'))


        authors = []
        for _ in range(AUTHOR_QTY):
            author = Author.objects.create(full_name=fake.name())   
            authors.append(author)

        self.stdout.write(self.style.SUCCESS(f'{len(authors)} genres created.'))


        books = []
        for _ in range(BOOK_QTY):
            cover_url = f"https://picsum.photos/seed/{uuid.uuid4()}/400/600"

            book = Book.objects.create(title=fake.sentence(nb_words=3).replace(".", ""),
                description=fake.text(max_nb_chars=300),
                publication_date=fake.date_between(start_date='-50y', end_date='-1y'),
                cover=cover_url, author=random.choice(authors), genre=random.choice(genres))

            books.append(book)

        self.stdout.write(self.style.SUCCESS(f'{len(books)} books created.'))


        book_copies = []
        for book in books:
            num_copies = random.randint(1,7)

            for _ in range(num_copies):
                status = random.choice([
                    BookCopy.Status.AVAILABLE,
                    BookCopy.Status.AVAILABLE,
                    BookCopy.Status.AVAILABLE,
                    BookCopy.Status.BORROWED,
                ]) 
                
                copy = BookCopy.objects.create(book=book, status=status)
                book_copies.append(copy)

        self.stdout.write(self.style.SUCCESS(f'{len(book_copies)} genres created.'))

        self.stdout.write(self.style.SUCCESS('Data seeding complete!'))


