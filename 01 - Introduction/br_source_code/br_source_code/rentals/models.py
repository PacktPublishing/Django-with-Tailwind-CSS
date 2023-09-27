from django.db import models
from books.models import Book
from customers.models import Customer
from datetime import timedelta
from .choices import STATUS_CHOICES
# Create your models here.

class Rental(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES)
    rent_start_date = models.DateField(help_text='when the book was rented')
    rent_end_date = models.DateField(help_text='deadline', blank=True)
    return_date = models.DateField(blank=True, null=True, help_text='actual return date')
    is_closed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.book.isbn} rented by {self.customer.username}"
    
    @property
    def status_text(self):
        statuses = dict(STATUS_CHOICES)
        return statuses[self.status]
    
    def save(self, *args, **kwargs):
        if not self.rent_end_date:
            self.rent_end_date = self.rent_start_date + timedelta(days=14)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('-created',)