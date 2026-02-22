from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class StudentProfile(models.Model):
    DOMAIN_CHOICES = [
        ('AI', 'Artificial Intelligence'),
        ('LAW', 'Law'),
        ('BIO', 'Biomedical'),
        ('ENG', 'Engineering'),
        ('ECE', 'Electronics and Communication'),
        ('OTHER', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    domain_interest = models.CharField(max_length=10, choices=DOMAIN_CHOICES, default='OTHER')
    skills = models.CharField(max_length=255, help_text="Comma-separated skills")
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    coding_performance = models.IntegerField(default=0, help_text="Score from 0-100 based on platform tasks")
    incoscore = models.IntegerField(default=0)
    
    def update_incoscore(self):
        """
        InCoScore = (Achievements * Weight) + (Coding Performance * Weight)
        """
        achievement_score = sum(a.score_value for a in self.achievements.all())
        new_score = achievement_score + (self.coding_performance * 5)
        self.incoscore = new_score
        self.save()

    def __str__(self):
        return self.user.username

class Achievement(models.Model):
    ACHIEVEMENT_TYPES = [
        ('HACKATHON', 'Hackathon'),
        ('INTERNSHIP', 'Internship'),
        ('RESEARCH', 'Research Paper'),
        ('COMPETITION', 'Competition Result'),
    ]
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=ACHIEVEMENT_TYPES)
    description = models.TextField()
    date_achieved = models.DateField()
    link = models.URLField(blank=True)
    score_value = models.IntegerField(default=50) # Increased base score for ranking significance

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.student.update_incoscore()

    def __str__(self):
        return f"{self.student.user.username} - {self.title}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        StudentProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
