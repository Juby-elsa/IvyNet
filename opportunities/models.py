from django.db import models
from accounts.models import StudentProfile

class University(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    logo_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name

class Opportunity(models.Model):
    DOMAIN_CHOICES = [
        ('AI', 'Artificial Intelligence'),
        ('LAW', 'Law'),
        ('BIO', 'Biomedical'),
        ('ENG', 'Engineering'),
        ('ECE', 'Electronics and Communication'),
        ('OTHER', 'Other'),
    ]
    
    title = models.CharField(max_length=300)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='opportunities')
    description = models.TextField()
    eligibility_criteria = models.TextField(blank=True, null=True)
    domain = models.CharField(max_length=10, choices=DOMAIN_CHOICES)
    link = models.URLField()
    location = models.CharField(max_length=255, blank=True)
    event_date = models.CharField(max_length=100, blank=True)
    deadline = models.DateTimeField(blank=True, null=True)
    posted_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Opportunities"

    def __str__(self):
        return f"{self.title} @ {self.university}"

class Application(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE)
    applied_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Applied') # Applied, Under Review, Accepted, Rejected
    
    def __str__(self):
        return f"{self.student.user.username} applied to {self.opportunity.title}"
