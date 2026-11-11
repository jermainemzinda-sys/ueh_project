from django.db import models
from django.contrib.auth.models import User

# 1. PROFILE - what role is this user? Client, Agent or Admin?
class Profile(models.Model):
    ROLE_CHOICES = [
        ('CLIENT', 'MSME Client'),
        ('AGENT', 'UEH Support Agent'),
        ('ADMIN', 'UEH Admin'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='CLIENT')
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

# 2. BUSINESS - the small business owned by a Client
class Business(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    industry = models.CharField(max_length=100)
    location = models.CharField(max_length=100, default='Eastern Cape')

    def __str__(self):
        return self.name

# 3. SERVICE REQUEST - Client asks for help, Agent fixes it
class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
    ]
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    description = models.TextField()
    urgency = models.CharField(max_length=10, default='Medium')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='OPEN')
    assigned_agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_requests')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.business.name} - {self.category} ({self.status})"

# 4. OPPORTUNITY - Funding, Tender or Training posted by Admin
class Opportunity(models.Model):
    TYPE_CHOICES = [
        ('FUNDING', 'Funding'),
        ('TENDER', 'Tender'),
        ('TRAINING', 'Training'),
    ]
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    description = models.TextField()
    deadline = models.DateField()
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# 5. APPLICATION - Client applies for an Opportunity
class Application(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    message = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.business.name} -> {self.opportunity.title}"