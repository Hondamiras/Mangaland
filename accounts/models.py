from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.hashers import make_password

User = get_user_model()

READING_STATUSES = (
    ("reading", "O'qilyapti"),
    ("planned", "O'qiyman"),
    ("completed", "O'qilgan"),
    ("favorite", "Yoqtirganim"),
)

class EmailVerificationCode(models.Model):
    user    = models.OneToOneField(User, on_delete=models.CASCADE)
    code    = models.CharField(max_length=6)
    created = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created + timedelta(minutes=15)

    def __str__(self):
        return f"{self.user.email} → {self.code}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reading_list = models.ManyToManyField(
        'manga.Manga',
        through='ReadingStatus',
        blank=True
    )

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profillar"

    def __str__(self):
        return self.user.username

    def add_to_reading_list(self, manga, status: str = "planned"):
        ReadingStatus.objects.update_or_create(
            user_profile=self,
            manga=manga,
            defaults={"status": status}
        )


class ReadingStatus(models.Model):
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='reading_statuses'
    )
    manga = models.ForeignKey(
        'manga.Manga',
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=15,
        choices=READING_STATUSES,
        default="planned"
    )

    class Meta:
        unique_together = ("user_profile", "manga")
        verbose_name = "O'qish holati"
        verbose_name_plural = "O'qish holatlari"

    def __str__(self):
        return f"{self.user_profile.user.username} — {self.manga.title} ({self.status})"


class PendingSignup(models.Model):
    username      = models.CharField(max_length=150, unique=True)
    email         = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=128)
    code          = models.CharField(max_length=6)
    created       = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created + timedelta(minutes=15)

    def save_password(self, raw_password):
        self.password_hash = make_password(raw_password)
