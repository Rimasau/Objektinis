import unittest
from main import Ship, Carrier, Battleship, Cruiser, Submarine, Destroyer

class TestShip(unittest.TestCase):    
    def setUp(self):
        """Kuria kiekviena klase"""
        self.carrier = Carrier()
        self.battleship = Battleship()
        self.cruiser = Cruiser()
        self.submarine = Submarine()
        self.destroyer = Destroyer()

class TestShip(unittest.TestCase):    
    def setUp(self):
        """Kuria kiekviena klase"""
        self.carrier = Carrier()
        self.battleship = Battleship()
        self.cruiser = Cruiser()
        self.submarine = Submarine()
        self.destroyer = Destroyer()
    
    def test_ship_sizes(self):
        """Tikrina ar laivas atitinka dydi"""
        self.assertEqual(self.carrier.size, 5, "Carrier dydis turi but 5")
        self.assertEqual(self.battleship.size, 4, "Battleship dydis turi but 4")
        self.assertEqual(self.cruiser.size, 3, "Cruiser dydis turi but 3")
        self.assertEqual(self.submarine.size, 3, "Submarine dydis turi but 3")
        self.assertEqual(self.destroyer.size, 2, "Destroyer dydis turi but 2")
    
    def test_initial_hit_count(self):
        """Tikrina ar laivai pradeda su 0 hitu"""
        for ship in [self.carrier, self.battleship, self.cruiser, 
                    self.submarine, self.destroyer]:
            self.assertEqual(ship.hit_count, 0, 
                           "Naujas laivas turi buti su 0 hit")
    
    def test_ship_sunk(self):
        """Tikrina ar laivas nuskendo"""
        self.assertFalse(self.destroyer.ship_sunk(), 
                        "Laivas turi buti nenuskendes")
        
        self.destroyer.hit_count += 1
        self.assertFalse(self.destroyer.ship_sunk(), 
                        "Po 1 smugio laivas turi buti nenuskendes (turi but 2)")
        
        self.destroyer.hit_count += 1
        self.assertTrue(self.destroyer.ship_sunk(), 
                       "Po 2 smugiu laivas turi nuskesti")
        
        self.destroyer.hit_count += 1
        self.assertTrue(self.destroyer.ship_sunk(), 
                       "Laivas nuskendes, nesvarbu ar bus smugis")
    
    def test_ship_hierarchy(self):
        """Tikrina ar visi laivai priklauso ship klasei"""
        for ship in [self.carrier, self.battleship, self.cruiser, 
                    self.submarine, self.destroyer]:
            self.assertIsInstance(ship, Ship, 
                                "Visi laivai turi paveldeti is ship")

if __name__ == '__main__':
    unittest.main()