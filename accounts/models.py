from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.template.loader import get_template
from django.urls import reverse
from django.utils import timezone
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from decrypto.utils import unique_key_generator, unique_slug_generator_by_email, random_string_generator


class EmailActivationQuerySet(models.query.QuerySet):
    def confirmable(self, DEFAULT_ACTIVATION_DAYS=7):
        now = timezone.now()
        start_range = now - timedelta(days=DEFAULT_ACTIVATION_DAYS)
        end_range = now
        return self.filter(activated=False, forced_expired=False).filter(timestamp__gt=start_range,
                                                                         timestamp__lte=end_range)


class EmailActivationManager(models.Manager):
    def get_queryset(self):
        return EmailActivationQuerySet(self.model, using=self._db)

    def confirmable(self):
        return self.get_queryset().confirmable()

    def email_exists(self, email):
        return self.get_queryset().filter(Q(email=email) | Q(user__email=email)).filter(activated=False)


class EmailActivation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    key = models.CharField(max_length=120, blank=True, null=True)
    activated = models.BooleanField(default=False)
    forced_expired = models.BooleanField(default=False)
    expires = models.IntegerField(default=7)  # 7 Days
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    objects = EmailActivationManager()

    def __str__(self):
        return self.email

    def can_activate(self):
        qs = EmailActivation.objects.filter(pk=self.pk).confirmable()  # 1 object
        return bool(qs.exists())

    def activate(self):
        if self.can_activate():
            # post activation signal for user
            self.activated = True
            self.save()
            return True
        return False

    def regenerate(self):
        self.key = None
        self.save()
        return self.key is not None

    def send_activation(self):
        if not self.activated and not self.forced_expired and self.key:
            base_url = getattr(settings, 'BASE_URL', 'https://api.decrypto.com')
            key_path = reverse("account-url:email-activate", kwargs={'key': self.key})  # use reverse
            path = "{base}{path}".format(base=base_url, path=key_path)
            context = {
                'path': path,
                'email': self.email
            }
            html_ = get_template("registration/emails/verify.html").render(context)
            subject = 'Decrypto Account Activation'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [self.email]

            from django.core.mail import EmailMessage
            message = EmailMessage(
                subject, html_, from_email, recipient_list
            )
            message.fail_silently = True
            # message.send()
        return False


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uuid = models.CharField(max_length=255, blank=True, null=True, unique=True)
    phone = PhoneNumberField(blank=True, null=True)
    country = CountryField(blank=True, null=True, max_length=255)
    country_flag = models.CharField(max_length=200, blank=True, null=True)
    ssn = models.CharField(blank=True, null=True, max_length=20,
                           help_text='Social Security Number/National Identity Number')
    trades = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "profile"
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        unique_together = ('phone', 'slug', 'uuid',)

    def __str__(self):
        return self.uuid

    def get_absolute_url(self):
        return reverse('account:profile-detail', kwargs={'slug': self.slug})

    def get_phone(self):
        if self.phone:
            return str(self.phone)
        return None

    def get_country(self):
        if self.country:
            return str(self.country.name)
        return None


def pre_save_email_activation(sender, instance, *args, **kwargs):
    if not instance.activated and not instance.forced_expired and not instance.key:
        instance.key = unique_key_generator(instance)


pre_save.connect(pre_save_email_activation, sender=EmailActivation)


def post_save_user_create_reciever(sender, instance, created, *args, **kwargs):
    if created:
        obj = EmailActivation.objects.create(user=instance, email=instance.email)
        obj.send_activation()
        Profile.objects.create(
            user=instance,
            slug=unique_slug_generator_by_email(instance),
            uuid=random_string_generator(12)
        )


post_save.connect(post_save_user_create_reciever, sender=User)

# class FavouriteAssets(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     favourite_coins = models.ManyToManyField(to='coins.Coin')
#     slug = models.SlugField(unique=True, blank=True, null=True)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         db_table = "favourite_assets"
#         verbose_name = "Favourite Asset"
#         verbose_name_plural = "Favourite Assets"
#         unique_together = ('user', 'slug',)
#
#     def __str__(self):
#         return str(self.user.username)
