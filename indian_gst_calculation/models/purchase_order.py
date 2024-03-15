# -*- coding: utf-8 -*-

from __future__ import division

from datetime import datetime
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
import decimal


class CustomPurchaseOrder(models.Model):
    """
        Adds three GST amount columns to purchase order models.
    """
    _inherit = "purchase.order"

    # import pdb; pdb.set_trace()

    CGST_SGST = fields.Boolean(string="CGST + SGST", store=True)
    IGST = fields.Boolean(string="IGST", store=True)
    UTGST = fields.Boolean(string="UTGST", store=True)
    no_gst = fields.Boolean(string="No GST", store=True, default=True)

    # Terms and Conditions
    contact_person_text = fields.Text(string="Contact Person")
    gst_text = fields.Text(string="GST")
    insurance_text = fields.Text(string="Insurance")
    delivery_term_text = fields.Text(string="Delivery Terms")
    packing_text = fields.Text(string="Packing Instructions")
    delivery_schedule_text = fields.Text(string="Delivery Schedule")
    terms_payment_text = fields.Text(string="Terms of Payment")
    documents_text = fields.Text(string="Documents")
    warranty_text = fields.Text(string="Warranty")
    special_text = fields.Text(string="Special Instructions 1")
    special_text_2 = fields.Text(string="Special Instructions 2")
    special_text_3 = fields.Text(string="Special Instructions 3")
    special_text_4 = fields.Text(string="Special Instructions 4")
    transportation_text = fields.Text(string="Transportation")

    @api.depends('order_line.price_total', 'CGST_SGST', 'IGST', 'UTGST', 'no_gst')
    def _amount_all(self):

        for order in self:
            amount_untaxed = amount_tax = 0.0
            total_gst = amount_CGST = amount_SGST = amount_IGST = amount_UTGST = 0.0
            C_S_GST_percent = I_GST_percent = UT_GST_percent = 0.0

            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                # FORWARDPORT UP TO 10.0
                if order.company_id.tax_calculation_rounding_method == 'round_globally':
                    taxes = line.taxes_id.compute_all(line.price_unit, line.order_id.currency_id, line.product_qty,
                                                      product=line.product_id, partner=line.order_id.partner_id)
                    amount_tax += sum(t.get('amount', 0.0) for t in taxes.get('taxes', []))
                else:
                    amount_tax += line.price_tax
                if order.no_gst == True:
                    amount_tax = 0.0

            if order.CGST_SGST == True:
                C_S_GST_percent = amount_tax / 2
                self.amount_IGST = self.amount_UTGST = 0.0
            elif order.IGST == True:
                I_GST_percent = amount_tax
                self.amount_CGST = self.amount_SGST = self.amount_UTGST = 0.0
            elif order.UTGST == True:
                UT_GST_percent = amount_tax
                self.amount_CGST = self.amount_SGST = self.amount_IGST = 0.0
            else:
                order.amount_tax = 0.0

            order.update({
                'amount_untaxed': order.currency_id.round(amount_untaxed),
                'amount_tax': order.currency_id.round(amount_tax),
                'amount_CGST': C_S_GST_percent,
                'amount_SGST': C_S_GST_percent,
                'amount_IGST': I_GST_percent,
                'amount_UTGST': UT_GST_percent,
                'amount_total': amount_untaxed + amount_tax,
            })

    amount_CGST = fields.Float(string="CGST", compute='_amount_all', store=True)
    amount_SGST = fields.Float(string="SGST", compute='_amount_all', store=True)
    amount_IGST = fields.Float(string="IGST", compute='_amount_all', store=True)
    amount_UTGST = fields.Float(string="UTGST", compute='_amount_all', store=True)


    def amount_to_text(self, amount, currency):
        convert_amount_in_words = currency.amount_to_text(amount)
        if decimal.Decimal(amount).as_tuple().exponent == 0:
            convert_amount_in_words = convert_amount_in_words.replace(' Cent', ' Only')
        else:
            convert_amount_in_words = convert_amount_in_words.replace(' Cents', ' Only')
        return convert_amount_in_words

    @api.model
    def create(self, vals):
        res = super(CustomPurchaseOrder, self).create(vals)
        if res.no_gst == True and res.CGST_SGST == True or res.IGST == True or res.UTGST == True:
            res.no_gst = False
        data = {'amount_CGST': res.amount_CGST,
                'amount_SGST': res.amount_SGST,
                'amount_IGST': res.amount_IGST,
                'amount_UTGST': res.amount_UTGST,
                'CGST_SGST': res.CGST_SGST,
                'IGST': res.IGST,
                'UTGST': res.UTGST,
                'no_gst': res.no_gst}
        res.write(data)
        return res

    def write(self, values):
        vals = super(CustomPurchaseOrder, self).write(values)
        if 'CGST_SGST' in values.keys():
            if values['CGST_SGST'] == True:
                self.IGST = self.UTGST = self.no_gst = False

        elif 'IGST' in values.keys():
            if values['IGST'] == True:
                self.CGST_SGST = self.UTGST = self.no_gst = False

        elif 'UTGST' in values.keys():
            if values['UTGST'] == True:
                self.IGST = self.CGST_SGST = self.no_gst = False

        elif 'no_gst' in values.keys():
            if values['no_gst'] == True:
                self.IGST = self.UTGST = self.CGST_SGST = False
        else:
            pass
        return vals

    def _prepare_invoice(self):
        res = super(CustomPurchaseOrder, self)._prepare_invoice()
        res['no_gst'] = self.no_gst
        res['CGST_SGST'] = self.CGST_SGST
        res['IGST'] = self.IGST
        res['UTGST'] = self.UTGST
        res['ref'] = self.name
        if self.bill_to:
            res['bill_to'] = self.bill_to.id
        if self.ship_to:
            res['ship_to'] = self.ship_to.id
        return res


class CustomPurchaseOrderLine(models.Model):
    """
        Takes tax percent to distribute as per GST selection type.
    """
    _inherit = 'purchase.order.line'

    @api.depends('product_id', 'order_id.CGST_SGST', 'order_id.IGST', 'order_id.UTGST', 'taxes_id')
    def _compute_gst_percentage(self):
        for order in self:
            total_gst = 0.0
            for line in order:
                for tax in line.taxes_id:
                    if tax.amount_type == "group":
                        for child_tax_amount in tax.children_tax_ids:
                            total_gst += child_tax_amount.amount
                        if order.order_id.CGST_SGST == True:
                            C_S_GST_percent = total_gst / 2
                            line.purchase_CGST = line.purchase_SGST = C_S_GST_percent
                            line.purchase_amount_CGST = line.price_subtotal * line.purchase_CGST / 100
                            line.purchase_amount_SGST = line.price_subtotal * line.purchase_SGST / 100
                        elif order.order_id.IGST == True:
                            I_GST_percent = total_gst
                            line.purchase_IGST = I_GST_percent
                            line.purchase_amount_IGST = line.price_subtotal * line.purchase_IGST / 100
                        elif order.order_id.UTGST == True:
                            UT_GST_percent = total_gst
                            line.purchase_UTGST = UT_GST_percent
                            line.purchase_amount_UTGST = line.price_subtotal * line.purchase_UTGST / 100
                        else:
                            line.purchase_CGST = line.purchase_SGST = 0.0
                            line.purchase_IGST = line.purchase_UTGST = 0.0
                        line.HSN_SAC = line.product_id.HSN_SAC

                    if tax.amount_type == "percent":
                        total_gst += tax.amount
                        if order.order_id.CGST_SGST == True:
                            CS_GST_percent = total_gst / 2
                            line.purchase_CGST = line.purchase_SGST = CS_GST_percent
                            line.purchase_amount_CGST = line.price_subtotal * line.purchase_CGST / 100
                            line.purchase_amount_SGST = line.price_subtotal * line.purchase_SGST / 100
                        elif order.order_id.IGST == True:
                            line.purchase_IGST = total_gst
                            line.purchase_amount_IGST = line.price_subtotal * line.purchase_IGST / 100
                        elif order.order_id.UTGST == True:
                            line.purchase_UTGST = total_gst
                            line.purchase_amount_UTGST = line.price_subtotal * line.purchase_UTGST / 100
                        else:
                            line.purchase_CGST = line.purchase_SGST = 0.0
                            line.purchase_IGST = line.purchase_UTGST = 0.0
                        line.HSN_SAC = line.product_id.HSN_SAC
                line.purchase_amount_TAX = line.purchase_CGST + line.purchase_SGST + line.purchase_IGST + line.purchase_UTGST

    purchase_CGST = fields.Float(string="CGST", compute='_compute_gst_percentage', store=True)
    purchase_SGST = fields.Float(string="SGST", compute='_compute_gst_percentage', store=True)
    purchase_IGST = fields.Float(string="IGST", compute='_compute_gst_percentage', store=True)
    purchase_UTGST = fields.Float(string="UTGST", compute='_compute_gst_percentage', store=True)
    HSN_SAC = fields.Char(string="HSN/SAC", compute='_compute_gst_percentage', store=True)
    no_gst = fields.Boolean(string="No GST")

    purchase_amount_CGST = fields.Float(string="CGST Amount", compute='_compute_gst_percentage', store=True)
    purchase_amount_SGST = fields.Float(string="CGST Amount", compute='_compute_gst_percentage', store=True)
    purchase_amount_IGST = fields.Float(string="CGST Amount", compute='_compute_gst_percentage', store=True)
    purchase_amount_UTGST = fields.Float(string="CGST Amount", compute='_compute_gst_percentage', store=True)

    purchase_amount_TAX = fields.Float(string="Tax Rate", compute='_compute_gst_percentage', store=True)

    def _prepare_account_move_line(self, move=False):
        self.ensure_one()
        res = {
            'display_type': self.display_type,
            'sequence': self.sequence,
            'name': '%s: %s' % (self.order_id.name, self.name),
            'product_id': self.product_id.id,
            'product_uom_id': self.product_uom.id,
            'quantity': self.qty_to_invoice,
            'price_unit': self.price_unit,
            'tax_ids': [(6, 0, self.taxes_id.ids)],
            'analytic_account_id': self.account_analytic_id.id,
            'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
            'purchase_line_id': self.id,
            'invoice_CGST': self.purchase_CGST,
            'invoice_SGST': self.purchase_SGST,
            'invoice_IGST': self.purchase_IGST,
            'invoice_UTGST': self.purchase_UTGST,
            'HSN_SAC': self.HSN_SAC,
            'no_gst': self.no_gst,
            'invoice_amount_CGST': self.purchase_amount_CGST,
            'invoice_amount_SGST': self.purchase_amount_SGST,
            'invoice_amount_IGST': self.purchase_amount_IGST,
            'invoice_amount_UTGST': self.purchase_amount_UTGST
        }
        if not move:
            return res

        if self.currency_id == move.company_id.currency_id:
            currency = False
        else:
            currency = move.currency_id

        res.update({
            'move_id': move.id,
            'currency_id': currency and currency.id or False,
            'date_maturity': move.invoice_date_due,
            'partner_id': move.partner_id.id,
        })
        return res

    @api.onchange('product_id', 'order_id.CGST_SGST', 'order_id.IGST', 'order_id.UTGST', 'order_id.no_gst')
    def onchange_product_id(self):
        result = {}
        if not self.product_id:
            return result

        # Reset date, price and quantity since _onchange_quantity will provide default values
        self.date_planned = datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        self.price_unit = self.product_qty = 0.0
        self.product_uom = self.product_id.uom_po_id or self.product_id.uom_id
        result['domain'] = {'product_uom': [('category_id', '=', self.product_id.uom_id.category_id.id)]}

        product_lang = self.product_id.with_context({
            'lang': self.partner_id.lang,
            'partner_id': self.partner_id.id,
        })
        self.name = product_lang.display_name
        if product_lang.description_purchase:
            self.name += '\n' + product_lang.description_purchase
        if self.order_id.no_gst == True:
            fpos = self.env['account.fiscal.position']
            if self.env.uid == SUPERUSER_ID:
                company_id = self.env.user.company_id.id
                self.taxes_id = self.env['account.tax']
            else:
                self.taxes_id = self.env['account.tax']
        else:
            fpos = self.order_id.fiscal_position_id
            if self.env.uid == SUPERUSER_ID:
                company_id = self.env.user.company_id.id
                self.taxes_id = fpos.map_tax(
                    self.product_id.supplier_taxes_id.filtered(lambda r: r.company_id.id == company_id))
            else:
                self.taxes_id = fpos.map_tax(self.product_id.supplier_taxes_id)
        self._suggest_quantity()
        self._onchange_quantity()

        return result