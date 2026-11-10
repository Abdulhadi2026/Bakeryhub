from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


def sync_user_role(user):
    profile = getattr(user, 'profile', None)
    role = getattr(profile, 'role', None) or 'staff'
    user.is_staff = role in {'admin', 'staff'}
    user.is_superuser = role == 'admin'
    User.objects.filter(pk=user.pk).update(
        is_staff=user.is_staff,
        is_superuser=user.is_superuser,
    )
    return user


class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('staff', 'Staff'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, default='')
    address = models.TextField(blank=True, default='')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='staff')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.role})"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    profile, _ = UserProfile.objects.get_or_create(user=instance)
    sync_user_role(instance)
    if not created:
        profile.save()
