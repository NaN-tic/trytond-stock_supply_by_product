# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from .configuration import *
from .stock_supply_by_product import *


def register():
    Pool.register(
        Configuration,
        PurchaseRequest,
        StockSupplyByProductWizardStart,
        module='stock_supply_by_product', type_='model')
    Pool.register(
        StockSupplyByProductWizard,
        module='stock_supply_by_product', type_='wizard')
