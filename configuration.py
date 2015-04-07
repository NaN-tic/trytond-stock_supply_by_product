# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval, Bool

__all__ = ['Configuration']
__metaclass__ = PoolMeta


class Configuration:
    __name__ = 'stock.configuration'
    compute_quantity_method = fields.Property(fields.Selection([
            ('quantity', 'Quantity'),
            ('forecast_quantity', 'Forecast Quantity'),
            ], 'Compute Quantity Method', states={
            'required': Bool(Eval('context', {}).get('company')),
            }))
