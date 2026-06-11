from django.contrib import admin, messages
from bookcopy.models import BookCopy


@admin.register(BookCopy)
class BookCopyAdmin(admin.ModelAdmin):
    list_display = ('book', 'status')
    list_filter = ('book', 'status')

    actions = ['make_available', 'make_borrowed']

    def make_available(self, request, queryset):
        rows_updated = queryset.update(status='dostępny')

        self.message_user(request, f'Zaktualizowano status {rows_updated} egzemplarzy', messages.SUCCESS)
    
    make_available.short_description = 'Oznacz zaznaczone jako dostępne'


    def make_borrowed(self, request, queryset):
        rows_updated = queryset.update(status='wypożyczony')

        self.message_user(request, f'Zaktualizowano status {rows_updated} egzemplarzy', messages.SUCCESS)
    
    make_borrowed.short_description = 'Oznacz zaznaczone jako wypożyczone'    