from django.db import models

class Worker(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Fingerprint(models.Model):
    worker = models.ForeignKey(Worker, related_name='fingerprints', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"Fingerprint of {self.worker.name}"