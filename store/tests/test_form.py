from django.test import TestCase
from django.urls import reverse
from store.models import Publisher, St, Genre, Review
from .game_factories import GameFactory, GenreFactory, PublisherFactory
from store.forms import ReviewForm


class ReviewFormTests(TestCase):
    def test_review_form_with_invalid_data(self):
        form = ReviewForm({
            'body': 'invalid body',
            'value': 'blalba'
        })
        self.assertFalse(form.is_valid())
        
    def test_review_form_with_valid_data(self):
        form = ReviewForm({
            'body': 'Отличный проект!',
            'value': 'up'
        })
        self.assertTrue(form.is_valid())
        
    def test_review_saved_in_db(self):
        form = ReviewForm({
            'body': 'Отличный проект!',
            'value': 'up'
        })
        review = form.save(commit=False)
        review.project = GameFactory()
        self.assertEqual(review.body, 'Отличный проект!')
        self.assertEqual(review.value, 'up')


        