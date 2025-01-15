from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from decimal import Decimal, ROUND_HALF_UP


class Profile(models.Model):
    ROLE_CHOICES = [
        ('LR', 'Lessor'),
        ('LE', 'Lessee'),
        ('SE', 'Seller'),
        ('AD', 'Admin')
    ]
    user = models.OneToOneField(
        User,
        related_name='profile',
        on_delete=models.CASCADE
    )
    display_name = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    role = models.CharField(
        max_length=2,
        choices=ROLE_CHOICES
    )

    def __str__(self):
        return self.display_name or self.user.username


class Contract(models.Model):
    lessor = models.ForeignKey(
        User,
        related_name='lessor_contracts',
        on_delete=models.CASCADE
    )
    lessee = models.ForeignKey(
        User,
        related_name='lessee_contracts',
        on_delete=models.CASCADE
    )
    seller = models.ForeignKey(
        User,
        related_name='seller_contracts',
        on_delete=models.CASCADE
    )
    number = models.CharField(max_length=30)
    meter = models.CharField(max_length=20)
    started = models.DateField()

    class Meta:
        ordering = ['-started', '-number']

    def get_absolute_url(self):
        return reverse('view_contract', args=[self.id])

    def __str__(self):
        return self.number


class FinanceDetails(models.Model):
    contract = models.ForeignKey(
        Contract,
        related_name='finance_details',
        on_delete=models.CASCADE
    )
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    upfront = models.DecimalField(max_digits=10, decimal_places=2)
    final_payment = models.DecimalField(max_digits=10, decimal_places=2)
    period = models.PositiveIntegerField()  # in month
    rate = models.DecimalField(max_digits=6, decimal_places=2)  # in percent
    vat_rate = models.DecimalField(max_digits=6, decimal_places=2)  # in percent

    @property
    def monthly_rate(self):
        return self.rate / 1200

    @property
    def monthly_payment(self):
        payment = ((self.cost - self.upfront - self.final_payment) *
                   self.monthly_rate / (1 - (1 + self.monthly_rate) ** (-1 * self.period)) * (1 + self.vat_rate / 100))
        payment = Decimal(payment)
        payment = payment.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return payment


class Payment(models.Model):
    contract = models.ForeignKey(
        Contract,
        related_name='payments',
        on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    paid = models.BooleanField(default=False)
    request_paid = models.BooleanField(default=False)

    class Meta:
        ordering = ['date']


class WarrantyCase(models.Model):
    STATUS_CHOICES = [
        ('CR', 'Создан'),
        ('IW', 'В процесссе'),
        ('CO', 'Решен'),
    ]
    contract = models.ForeignKey(
        Contract,
        related_name='warranty_cases',
        on_delete=models.CASCADE
    )
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    resolved = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default='CR'
    )
