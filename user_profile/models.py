from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

from os_project.models import Project


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    image = CloudinaryField("image", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("profile_detail", kwargs={"username": self.user.username})

    def __str__(self):
        return f"{self.user.username}'s profile"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)


class WomenInTech(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="women_in_tech_profile"
    )
    image = CloudinaryField("image", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # role fields
    is_woman_in_tech = models.BooleanField(default=False)

    # skills fields
    tech_specialties = models.CharField(max_length=200, blank=True)
    years_of_experience = models.IntegerField(null=True, blank=True)

    # Maintainer fields
    github_username = models.CharField(max_length=100, blank=True)
    maintained_projects = models.ManyToManyField(
        Project, blank=True
    )  # Need to create project model
    favourite_projects = models.ManyToManyField(
        Project,
        through="FavouriteProjectWIT",
        related_name="favourited_by_wit",
        blank=True,
    )
    contribution_focus = models.ManyToManyField(
        Project,
        through="ContributionFocusWIT",
        related_name="focused_by_wit",
        blank=True,
    )

    # Additional fields
    about = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse("profile_detail", kwargs={"username": self.user.username})

    def __str__(self):
        return f"{self.user.username}'s profile"


class OS_Maintainer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="os_maintainer_profile"
    )
    image = CloudinaryField("image", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # role fields
    is_os_maintainer = models.BooleanField(default=False)

    # Maintainer fields
    github_username = models.CharField(max_length=100, blank=True)
    maintained_projects = models.ManyToManyField(
        Project, blank=True
    )  # Need to create project model
    favourite_projects = models.ManyToManyField(
        Project,
        through="FavouriteProjectOS",
        related_name="favourited_by_os",
        blank=True,
    )
    contribution_focus = models.ManyToManyField(
        Project,
        through="ContributionFocusOS",
        related_name="focused_by_os",
        blank=True,
    )

    # Additional fields
    about = models.TextField(blank=True)
    sponsored_projects = models.ManyToManyField(
        Project, related_name="sponsored_by", blank=True
    )

    def get_absolute_url(self):
        return reverse("os_profile_detail", kwargs={"username": self.user.username})

    def __str__(self):
        return f"{self.user.username}'s OS Maintainer profile"


class FavouriteProjectWIT(models.Model):
    wit = models.ForeignKey(WomenInTech, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("wit", "project")

    def __str__(self):
        return f"{self.wit.user.username} favourited {self.project.title}"


class ContributionFocusWIT(models.Model):
    wit = models.ForeignKey(WomenInTech, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    focus_area = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("wit", "project")

    def __str__(self):
        return f"{self.wit.user.username} focuses on {self.focus_area} for {self.project.title}"


class FavouriteProjectOS(models.Model):
    maintainer = models.ForeignKey(OS_Maintainer, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("maintainer", "project")

    def __str__(self):
        return f"{self.maintainer.user.username} favourited {self.project.title}"


class ContributionFocusOS(models.Model):
    maintainer = models.ForeignKey(OS_Maintainer, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    focus_area = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("maintainer", "project")

    def __str__(self):
        return f"{self.maintainer.user.username} focuses on {self.focus_area} for {self.project.title}"
