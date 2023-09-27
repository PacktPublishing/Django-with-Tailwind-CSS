from django.db import models
from publishers.models import Publisher
from authors.models import Author
from django.utils.text import slugify
import uuid
from django.urls import reverse
# imports for qrcode generation
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image
from rentals.choices import STATUS_CHOICES
from .utils import hash_book_info
# Create your models here.

class BookTitle(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(blank=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def books(self):
        return self.book_set.all()
    
    def get_absolute_url(self):
        letter = self.title[:1].lower()
        return reverse("books:detail", kwargs={"letter": letter, "slug": self.slug})
    
    def __str__(self):
        return f"Book position: {self.title}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Book(models.Model):
    """
    curent status for books
    id: 1,2,3 ...
    isbn: unique 24 character long string

    future state
    id: 36 character long string
    isbn: hashed string based on book title & publisher name
    many BOOKS can have the SAME ISBN
    """
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, editable=False)
    title = models.ForeignKey(BookTitle, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=24, blank=True)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        letter = self.title.title[:1].lower()
        return reverse("books:detail-book", kwargs={"letter": letter, "slug": self.title.slug, "book_id": self.id})
    
    def delete_object(self):
        letter = self.title.title[:1].lower()
        return reverse('books:delete-book', kwargs={'letter':letter, 'slug': self.title.slug, "book_id": self.id})

    def __str__(self):
        return str(self.title)
    
    @property
    def status(self):
        if len(self.rental_set.all()) > 0:
            statuses = dict(STATUS_CHOICES)
            return statuses[self.rental_set.first().status]
        return False
    
    @property
    def rental_id(self):
        if len(self.rental_set.all()) > 0:
            return self.rental_set.first().id
        return None
    
    @property
    def is_available(self):
        if len(self.rental_set.all()) > 0:
            status = self.rental_set.first().status
            return True if status == '#1' else False
        return True

    def save(self, *args, **kwargs):
        if not self.isbn:
            # self.isbn = str(uuid.uuid4()).replace('-', '')[:24].lower()
            self.isbn = hash_book_info(self.title.title, self.title.publisher.name)

            # generate qr code
            qrcode_img = qrcode.make(self.isbn)
            canvas = Image.new('RGB', (qrcode_img.pixel_size, qrcode_img.pixel_size), 'white')
            canvas.paste(qrcode_img)
            fname = f'qr_code-{self.isbn}.png'
            buffer = BytesIO()
            canvas.save(buffer, 'PNG')
            self.qr_code.save(fname, File(buffer), save=False)
            canvas.close()

        super().save(*args, **kwargs)
