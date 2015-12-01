# This file is part of the stock_supply_by_product module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class StockSupplyByProductTestCase(ModuleTestCase):
    'Test Stock Supply By Product module'
    module = 'stock_supply_by_product'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        StockSupplyByProductTestCase))
    return suite
