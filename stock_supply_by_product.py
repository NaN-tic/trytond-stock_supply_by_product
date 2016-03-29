# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelView, fields
from trytond.pool import PoolMeta, Pool
from trytond.pyson import PYSONEncoder
from trytond.transaction import Transaction
from trytond.wizard import Wizard, StateView, Button, StateAction


__all__ = ['PurchaseRequest', 'StockSupplyByProductWizardStart',
    'StockSupplyByProductWizard']


class PurchaseRequest:
    __metaclass__ = PoolMeta
    __name__ = 'purchase.request'

    @classmethod
    def _get_origin(cls):
        origins = super(PurchaseRequest, cls)._get_origin()
        origins.add('product.product')
        return origins


class StockSupplyByProductWizardStart(ModelView):
    'Stock Supply By Product Wizard Start'
    __name__ = 'stock.supply.by.product.wizard.start'
    warehouse = fields.Many2One('stock.location', 'Warehouse',
        domain=[('type', '=', 'warehouse')], required=True)
    supplier = fields.Many2One('party.party', 'Supplier')

    @staticmethod
    def default_warehouse():
        Warehouse = Pool().get('stock.location')
        warehouses = Warehouse.search([
                ('type', '=', 'warehouse'),
                ])
        if len(warehouses) == 1:
            return warehouses[0].id


class StockSupplyByProductWizard(Wizard):
    'Stock Supply By Product Wizard'
    __name__ = 'stock.supply.by.product.wizard'
    start = StateView('stock.supply.by.product.wizard.start',
        'stock_supply_by_product.'
        'stock_supply_by_product_wizard_start_view_form', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Create', 'request', 'tryton-ok', default=True),
            ])
    request = StateAction('stock_supply.act_purchase_request_form')

    def do_request(self, action):
        pool = Pool()
        PurchaseRequest = pool.get('purchase.request')
        Product = pool.get('product.product')
        Configuration = pool.get('stock.configuration')

        context = Transaction().context
        products = context.get('active_ids')
        products = Product.browse(products)
        supplier = self.start.supplier
        compute_quantity_method = Configuration(1).compute_quantity_method

        vlist = []
        for product in products:
            if not product.purchasable:
                continue
            quantity = getattr(product, compute_quantity_method)
            values = {
                'product': product.id,
                'party': supplier.id if supplier else None,
                'quantity': 1,
                'uom': product.default_uom.id,
                'computed_quantity': quantity,
                'computed_uom': product.default_uom.id,
                'warehouse': self.start.warehouse.id,
                'origin': 'product.product,%s' % product.id,
                'company': context['company'],
                }
            vlist.append(values)
        PurchaseRequest.create(vlist)
        action['pyson_domain'] = PYSONEncoder().encode([
                ('purchase_line', '=', None),
                ])
        return action, {}

    def transition_request(self):
        return 'end'
