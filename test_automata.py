import unittest

from automata import LangtonsAnt, Life


class AutomataTests(unittest.TestCase):
    def test_ant_turns_flips_and_wraps(self):
        ant = LangtonsAnt(3, 3)
        ant.step()
        self.assertEqual(ant.cells, {(1, 1)})
        self.assertEqual(ant.position, (2, 1))
        ant.step()
        self.assertEqual(ant.position, (2, 0))

    def test_life_blinker(self):
        life = Life(5, 5, {(1, 2), (2, 2), (3, 2)})
        life.step()
        self.assertEqual(life.cells, {(2, 1), (2, 2), (2, 3)})
        life.step()
        self.assertEqual(life.cells, {(1, 2), (2, 2), (3, 2)})

    def test_life_wraps_at_boundary(self):
        life = Life(5, 5, {(4, 2), (0, 2), (1, 2)})
        life.step()
        self.assertEqual(life.cells, {(0, 1), (0, 2), (0, 3)})

    def test_invalid_boards(self):
        with self.assertRaises(ValueError):
            LangtonsAnt(0, 4)
        with self.assertRaises(ValueError):
            Life(2, 2, set())
        with self.assertRaises(ValueError):
            Life(5, 5, {(5, 0)})


if __name__ == "__main__":
    unittest.main()
