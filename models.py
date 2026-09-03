from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    ROLE_ADMIN = 'admin'
    ROLE_STUDENT = 'student'
    ROLE_TEACHER = 'teacher'
    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_STUDENT, 'Student'),
        (ROLE_TEACHER, 'Teacher'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    class_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"


class ModuleContent(models.Model):
    MODULE_CURRICULUM = 'curriculum'
    MODULE_STUDY_MATERIAL = 'study-material'
    MODULE_NOTIFICATION = 'notification'
    MODULE_EXAM = 'exam'
    MODULE_CHOICES = [
        (MODULE_CURRICULUM, 'Curriculum'),
        (MODULE_STUDY_MATERIAL, 'Study Material'),
        (MODULE_NOTIFICATION, 'Notification'),
        (MODULE_EXAM, 'Exam'),
    ]

    module_type = models.CharField(max_length=30, choices=MODULE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.FileField(upload_to='module_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_module_type_display()} - {self.title}"

    @property
    def file_name(self):
        if not self.image:
            return ''
        return self.image.name.split('/')[-1]

    @property
    def is_pdf(self):
        if not self.image:
            return False
        return self.image.name.lower().endswith('.pdf')

    @property
    def is_image(self):
        if not self.image:
            return False
        allowed_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp')
        return self.image.name.lower().endswith(allowed_extensions)
