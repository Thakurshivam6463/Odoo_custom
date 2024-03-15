from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class StockMove(models.Model):
    _inherit = 'stock.move'

    sample_id = fields.Many2one("sample.form", string="Sample")

class SampleRequestLine(models.Model):
    _inherit = 'project.project'

    product_ids = fields.One2many("product.move.line", "product_line_id", string="Sample")

class ProductMoveLine(models.Model):
    _name = 'product.move.line'

    product_id = fields.Many2one('product.product', string="Product  ")
    source_location = fields.Many2one('stock.location', string="Source Location ")
    destination_location = fields.Many2one('stock.location', string='Destination Location')
    qty = fields.Float(string='Quantity')

    product_line_id = fields.Many2one('project.project', string="Product Line", invisible=True)


