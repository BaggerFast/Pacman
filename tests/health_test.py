from unittest import TestCase

from game import Game
from objects import Health


class TestHealth(TestCase):
    game = Game()

    def test_constructor(self):
        self.assertRaises(Exception, Health(self.game, 0, 3))
        self.assertRaises(Exception, Health(self.game, 4, 3))

    def test_minimal_bound(self):
        hp = Health(self.game, 0, 3)
        hp -= 1
        self.assertEqual(hp.count, 0)

    def test_maximum_bound(self):
        hp = Health(self.game, 3, 3)
        hp += 1
        self.assertEqual(hp.count, 3)

    def test_reduction(self):
        hp = Health(self.game, 2, 3)
        hp += 1
        self.assertEqual(hp.count, 3)

    def test_increase(self):
        hp = Health(self.game, 2, 3)
        hp -= 1
        self.assertEqual(hp.count, 1)

    def test_alive(self):
        hp = Health(self.game, 1, 3)
        hp -= 1
        self.assertTrue(hp.alive)
