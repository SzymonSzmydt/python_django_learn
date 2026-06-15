from django.views import View
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from datetime import timedelta
from bookcopy.models import BookCopy
from reservation.models import Reservation
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.db import transaction
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def register(request):
    """
    Widok odpowiedzialny za rejestrację nowego użytkownika.

    Funkcjonalności:
    - wyświetlanie formularza rejestracyjnego,
    - walidacja danych przesłanych metodą POST,
    - tworzenie nowego użytkownika,
    - wyświetlanie komunikatu o poprawnej rejestracji,
    - przekierowanie do strony logowania po sukcesie.
    """

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')

            messages.success(
                request,
                f"Konto dla {username} zostało utworzone! Możesz się zalogować."
            )

            return redirect('login/')
    else:
        form = UserCreationForm()

    return render(request, 'users/register.html', {'form': form})


class ReserveBookView(LoginRequiredMixin, View):
    """
    Widok odpowiedzialny za rezerwację egzemplarza książki
    przez zalogowanego użytkownika.

    Funkcjonalności:
    - blokowanie rekordu egzemplarza książki podczas rezerwacji,
    - sprawdzanie dostępności egzemplarza,
    - tworzenie rezerwacji na 14 dni,
    - aktualizacja statusu egzemplarza na BORROWED,
    - przekierowanie użytkownika do dashboardu.
    """

    def post(self, request, pk):
        """
        Obsługuje żądanie POST odpowiedzialne za utworzenie rezerwacji.

        Parametry:
            pk (int): identyfikator egzemplarza książki.

        Returns:
            HttpResponseRedirect: przekierowanie do dashboardu
            lub strony szczegółów książki.
        """

        with transaction.atomic():
            copy = (
                BookCopy.objects
                .select_for_update()
                .get(pk=pk)
            )

            if copy.status != BookCopy.Status.AVAILABLE:
                return redirect("book_detail", pk=copy.book.id)

            Reservation.objects.create(
                user=request.user,
                bookcopy=copy,
                reservation_date=timezone.now().date(),
                expiration_date=timezone.now().date() + timedelta(days=14)
            )

            copy.status = BookCopy.Status.BORROWED
            copy.save(update_fields=["status"])

        return redirect("dashboard")


class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Widok dashboardu użytkownika.

    Funkcjonalności:
    - wyświetlanie aktywnych rezerwacji zalogowanego użytkownika,
    - filtrowanie rezerwacji po dacie wygaśnięcia.
    """

    template_name = "users/dashboard.html"

    def get_context_data(self, **kwargs):
        """
        Dodaje do kontekstu aktywne rezerwacje użytkownika.

        Returns:
            dict: kontekst przekazywany do template.
        """

        context = super().get_context_data(**kwargs)

        today = timezone.now().date()

        reservations = (
            Reservation.objects
            .filter(user=self.request.user)
            .select_related("bookcopy__book")
        )

        context["active_reservations"] = reservations.filter(
            expiration_date__gte=today
        )

        return context


class ReservationListView(ListView):
    """
    Widok wyświetlający listę wszystkich rezerwacji.

    Funkcjonalności:
    - pobieranie rezerwacji wraz z użytkownikiem i książką,
    - przekazywanie aktualnej daty do template,
    - optymalizacja zapytań do bazy danych.
    """

    model = Reservation
    template_name = "reservations/reservations_list.html"
    context_object_name = "reservations"

    def get_queryset(self):
        """
        Zwraca queryset rezerwacji wraz z powiązanymi relacjami.

        Returns:
            QuerySet: lista rezerwacji.
        """

        return (
            Reservation.objects
            .select_related("user", "bookcopy__book")
        )

    def get_context_data(self, **kwargs):
        """
        Dodaje aktualną datę do kontekstu template.

        Returns:
            dict: kontekst przekazywany do template.
        """

        context = super().get_context_data(**kwargs)
        context["today"] = timezone.now().date()

        return context


class CancelReservationView(LoginRequiredMixin, View):
    def post(self, request, pk):
        try:
            reservation = Reservation.objects.select_related("bookcopy").get(
                pk=pk,
                user=request.user
            )
        except Reservation.DoesNotExist:
            return redirect("dashboard")

        with transaction.atomic():
            copy = reservation.bookcopy
            copy.status = BookCopy.Status.AVAILABLE
            copy.save(update_fields=["status"])

            reservation.delete()

        return redirect("dashboard")

