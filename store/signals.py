from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Review
from .task import update_vote_count

@receiver(post_save, sender=Review)
def review_post_save(sender, instance, created, **kwargs):
    if created:
        update_vote_count.delay(instance.project.id)