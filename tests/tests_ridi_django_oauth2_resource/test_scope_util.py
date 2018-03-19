from django.test import TestCase

from ridi_oauth2.resource.constants import Scope
from ridi_oauth2.resource.scope_checker import ScopeChecker


class ScopeUtilTestCase(TestCase):
    def setUp(self):
        self.all_scope = [Scope.ALL]

    def test_scope_all(self):
        self.assertTrue(ScopeChecker.check(require_scopes=['user_info', ], user_scopes=self.all_scope))
        self.assertTrue(ScopeChecker.check(require_scopes=['book_data'], user_scopes=self.all_scope))
        self.assertTrue(ScopeChecker.check(require_scopes=['user_info', 'book_data'], user_scopes=self.all_scope))
        self.assertTrue(ScopeChecker.check(
            require_scopes=['user_info', 'book_data', 'notification', 'purchase_item'],
            user_scopes=self.all_scope)
        )

    def test_empty_require_scope(self):
        self.assertTrue(ScopeChecker.check(require_scopes=[], user_scopes=self.all_scope))
        self.assertTrue(ScopeChecker.check(require_scopes=[], user_scopes=['user_info']))
        self.assertTrue(ScopeChecker.check(require_scopes=[], user_scopes=['user_info', 'book_data']))

    def test_restrictive_scope(self):
        user_scopes = ['user_info', 'book_data', 'notification']

        self.assertTrue(ScopeChecker.check(require_scopes=['user_info', ], user_scopes=user_scopes))
        self.assertTrue(ScopeChecker.check(require_scopes=['user_info', 'book_data', ], user_scopes=user_scopes))
        self.assertTrue(ScopeChecker.check(require_scopes=['user_info', 'book_data', 'notification'], user_scopes=user_scopes))

        self.assertFalse(ScopeChecker.check(require_scopes=['purchase_item', ], user_scopes=user_scopes))
