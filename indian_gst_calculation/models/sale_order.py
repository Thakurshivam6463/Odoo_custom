# -*- coding: utf-8 -*-

from __future__ import division

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_compare
import decimal

class CustomSalesOrder(models.Model):

    """
        Adds three GST amount columns to sale order models.
    """
    _inherit = "sale.order"

    CGST_SGST = fields.Boolean(string="CGST + SGST", store=True)
    IGST = fields.Boolean(string="IGST", store=True)
    UTGST = fields.Boolean(string="UTGST", store=True)
    no_gst = fields.Boolean(string="No GST", store=True, default=True)

    @api.depends('order_line.price_total', 'CGST_SGST', 'IGST', 'UTGST', 'no_gst')
    def _amount_all(self):
        """
        Compute the total amount and GST amount of the SO.
        """
        for order in self:
            amount_untaxed = amount_tax = 0.0
            total_gst = amount_CGST = amount_SGST = amount_IGST = amount_UTGST = 0.0
            C_S_GST_percent = I_GST_percent = UT_GST_percent = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal

                if order.company_id.tax_calculation_rounding_method == 'round_globally':
                    price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                    taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty,
                                                    product=line.product_id, partner=line.order_id.partner_shipping_id)

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
                'amount_untaxed': amount_untaxed,
                'amount_tax': amount_tax,
                # 'amount_untaxed': order.pricelist_id.currency_id.round(amount_untaxed),
                # 'amount_tax': order.pricelist_id.currency_id.round(amount_tax),
                'amount_CGST': C_S_GST_percent,
                'amount_SGST': C_S_GST_percent,
                'amount_IGST': I_GST_percent,
                'amount_UTGST': UT_GST_percent,
                'amount_total': amount_untaxed + amount_tax
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
    def create(self, values):

        res = super(CustomSalesOrder, self).create(values)
        print("Printing res")
        print(res)
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

    def action_view_delivery(self):
        is_hsn = False
        for line in self.order_line:
            if not line.HSN_SAC:
                is_hsn = True
                break

        
        if is_hsn or  self.amount_total > (self.avail_limit + self.amount_total):
            raise UserError(_("HSC code can not be found in Products line."))
        res = super(CustomSalesOrder, self).action_view_delivery()
        return res



    def write(self, values):

        vals = super(CustomSalesOrder, self).write(values)
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
        res = super(CustomSalesOrder, self)._prepare_invoice()
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


class CustomSalesOrderLine(models.Model):
    """
        Takes tax percent to distribute as per GST selection type.
    """
    _inherit = "sale.order.line"

    @api.depends('product_id', 'order_id.CGST_SGST', 'order_id.IGST', 'order_id.UTGST')
    def _compute_gst_percentage(self):
        for order in self:
            total_gst = 0.0
            for line in order:
                for tax in line.tax_id:
                    if tax.amount_type == "group":
                        for child_tax_amount in tax.children_tax_ids:
                            total_gst += child_tax_amount.amount
                        if order.order_id.CGST_SGST == True:
                            CS_GST_percent = total_gst / 2
                            line.sale_CGST = line.sale_SGST = CS_GST_percent
                            line.sale_amount_CGST = line.price_subtotal * line.sale_CGST/100
                            line.sale_amount_SGST = line.price_subtotal * line.sale_SGST/100
                        elif order.order_id.IGST == True:
                            line.sale_IGST = total_gst
                            line.sale_amount_IGST = line.price_subtotal * line.sale_IGST/100
                        elif order.order_id.UTGST == True:
                            line.sale_UTGST = total_gst
                            line.sale_amount_UTGST = line.price_subtotal * line.sale_UTGST/100
                        else:
                            line.sale_CGST = line.sale_SGST = 0.0
                            line.sale_IGST = line.sale_UTGST = 0.0
                        line.HSN_SAC = line.product_id.HSN_SAC

                    if tax.amount_type == "percent":
                        total_gst += tax.amount
                        if order.order_id.CGST_SGST == True:
                            CS_GST_percent = total_gst / 2
                            line.sale_CGST = line.sale_SGST = CS_GST_percent
                            line.sale_amount_CGST = line.price_subtotal * line.sale_CGST/100
                            line.sale_amount_SGST = line.price_subtotal * line.sale_SGST/100
                        elif order.order_id.IGST == True:
                            line.sale_IGST = total_gst
                            line.sale_amount_IGST = line.price_subtotal * line.sale_IGST/100
                        elif order.order_id.UTGST == True :
                            line.sale_UTGST = total_gst
                            line.sale_amount_UTGST = line.price_subtotal * line.sale_UTGST/100
                        else:
                            line.sale_CGST = line.sale_SGST = 0.0
                            line.sale_IGST = line.sale_UTGST = 0.0
                        line.HSN_SAC = line.product_id.HSN_SAC
                line.sale_amount_TAX = line.sale_CGST + line.sale_SGST + line.sale_IGST + line.sale_UTGST

    sale_CGST = fields.Float(string="CGST", compute='_compute_gst_percentage', store=True)
    sale_SGST = fields.Float(string="SGST", compute='_compute_gst_percentage', store=True)
    sale_IGST = fields.Float(string="IGST", compute='_compute_gst_percentage', store=True)
    sale_UTGST = fields.Float(string="UTGST", compute='_compute_gst_percentage', store=True)
    HSN_SAC = fields.Char(string="HSN/SAC", compute='_compute_gst_percentage', store=True)
    no_gst = fields.Boolean(string="No GST")

    sale_amount_CGST = fields.Float(string="CGST Amount", compute='_compute_gst_percentage', store=True)
    sale_amount_SGST = fields.Float(string="SGST Amount", compute='_compute_gst_percentage', store=True)
    sale_amount_IGST = fields.Float(string="IGST Amount", compute='_compute_gst_percentage', store=True)
    sale_amount_UTGST = fields.Float(string="UTGST Amount", compute='_compute_gst_percentage', store=True)

    sale_amount_TAX = fields.Float(string="Tax Rate", compute='_compute_gst_percentage', store=True)




    def _compute_tax_id(self):
        for line in self:
            if self.order_id.no_gst == False:
                fpos = line.order_id.fiscal_position_id or line.order_id.partner_id.property_account_position_id
                # If company_id is set, always filter taxes by the company
                taxes = line.product_id.taxes_id.filtered(lambda r: not line.company_id or r.company_id == line.company_id)
                line.tax_id = fpos.map_tax(taxes, line.product_id, line.order_id.partner_shipping_id) if fpos else taxes
            else:
                fpos = self.env['account.fiscal.position']
                taxes = self.env['account.tax']
                line.tax_id = fpos.map_tax(taxes, line.product_id, line.order_id.partner_shipping_id) if fpos else taxes


    @api.onchange('product_id', 'order_id.CGST_SGST', 'order_id.IGST', 'order_id.UTGST', 'order_id.no_gst')
    def product_id_change(self):
        if not self.product_id:
            return {'domain': {'product_uom': []}}
        vals = {}
        domain = {'product_uom': [('category_id', '=', self.product_id.uom_id.category_id.id)]}
        if not self.product_uom or (self.product_id.uom_id.id != self.product_uom.id):
            vals['product_uom'] = self.product_id.uom_id
            vals['product_uom_qty'] = 1.0
        product = self.product_id.with_context(
            lang=self.order_id.partner_id.lang,
            partner=self.order_id.partner_id.id,
            quantity=vals.get('product_uom_qty') or self.product_uom_qty,
            date=self.order_id.date_order,
            pricelist=self.order_id.pricelist_id.id,
            uom=self.product_uom.id
        )
        name = product.name_get()[0][1]
        if product.description_sale:
            name += '\n' + product.description_sale
        vals['name'] = name

        self._compute_tax_id()

        if self.order_id.pricelist_id and self.order_id.partner_id:
            if self.order_id.no_gst == False and 'price_unit' not in vals.keys():
                vals['price_unit'] = self.env['account.tax']._fix_tax_included_price(self._get_display_price(product), product.taxes_id, self.tax_id)
            else:
                vals['price_unit'] = self._get_display_price(product)
        #Overwrite price from kel_pricing
        price = self.env['kel_pricing.kel_pricing'].sudo().search_read([('MATERIAL_NO','=',product.code),
                                                            ('REGION_CODE','=',self.order_id.partner_id.regio.zfill(2))])
        vals['price_unit'] = price[0]['MATERIAL_PRICE'] if len(price) > 0 else 0
            
        self.update(vals)
        title = False
        message = False
        warning = {}
        if product.sale_line_warn != 'no-message':
            title = _("Warning for %s") % product.name
            message = product.sale_line_warn_msg
            warning['title'] = title
            warning['message'] = message
            if product.sale_line_warn == 'block':
                self.product_id = False
            return {'warning': warning}
        return {'domain': domain}