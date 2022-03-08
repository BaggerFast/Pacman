from unittest import TestCase, main
from objects.health_controller import HealthLogic


class TestHealth(TestCase):

    # def test_constructor(self):
    #     self.assertRaises(Exception, HealthLogic(0, 3))
    #     self.assertRaises(Exception, HealthLogic(4, 3))

    # def test_minimal_bound(self):
    #     hp = HealthLogic(0, 3)
    #     hp.get_damage(1)
    #     self.assertEqual(hp.count, 0)

    def test_maximum_bound(self):
        hp = HealthLogic(3, 3)
        hp.get_health(1)
        self.assertEqual(hp.count, 3)

    def test_reduction(self):
        hp = HealthLogic(2, 3)
        hp.get_health(1)
        self.assertEqual(hp.count, 3)

    def test_increase(self):
        hp = HealthLogic(2, 3)
        hp.get_damage(1)
        self.assertEqual(hp.count, 1)

    def test_alive(self):
        hp = HealthLogic(1, 3)
        hp.get_damage(1)
        self.assertFalse(hp.alive)


if __name__ == '__main__':
    main()
