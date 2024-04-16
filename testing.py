import unittest
from main import massive_changes

class TestMassiveChanges(unittest.TestCase):
    def setUp(self) -> None:
        self.path1 = r"C:\Users\dacan\OneDrive\Desktop\PRUEBAS\Maxima Entropia\1 PROYECTO SURCO\6. Sub Area Vissim\Sub Area 016\Balanceado\Tipico\Manana\PTV Vissim Sub Area 016 Bal (SA).inpx"
        self.path2 = r"C:\Users\dacan\OneDrive\Desktop\PRUEBAS\Maxima Entropia\1 PROYECTO SURCO\6. Sub Area Vissim\Sub Area 016\Balanceado\Tipico\Noche\PTV Vissim Sub Area 016 Bal (SA).inpx"
        self.path3 = r"C:\Users\dacan\OneDrive\Desktop\PRUEBAS\Maxima Entropia\1 PROYECTO SURCO\6. Sub Area Vissim\Sub Area 016\Balanceado\Tipico\Tarde\PTV Vissim Sub Area 016 Bal (SA).inpx"

    def test_1(self):
        result = massive_changes(self.path1)
        self.assertIsNone(result, f"Fail")

    def test_2(self):
        result = massive_changes(self.path2)
        self.assertIsNone(result, f"Fail")

    def test_3(self):
        result = massive_changes(self.path3)
        self.assertIsNone(result, f"Fail")

if __name__ == '__main__':
    unittest.main()