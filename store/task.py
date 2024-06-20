from celery import shared_task
from .models import St

@shared_task
def update_vote_count(st_id):
    try:
        st = St.objects.get(id=st_id)
        reviews = st.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()
        ratio = (upVotes / totalVotes) * 100 if totalVotes > 0 else 0
        st.total_votes = totalVotes
        st.votes_ratio = ratio
        st.save()
    except St.DoesNotExist:
        pass
