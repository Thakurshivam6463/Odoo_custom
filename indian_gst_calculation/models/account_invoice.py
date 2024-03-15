# -*- coding: utf-8 -*-

from __future__ import division

from odoo import models, fields, api
from odoo.tools import float_is_zero, float_compare
import decimal


class CustomAccountInvoice(models.Model):
    """
        Adds three GST amount columns to sale order models.
    """
    _inherit = "account.move"

    CGST_SGST = fields.Boolean(string="CGST + SGST")
    IGST = fields.Boolean(string="IGST")
    UTGST = fields.Boolean(string="UTGST")
    no_gst = fields.Boolean(string="No GST", default=True)
    bill_to = fields.Many2one('res.partner',string="Bill To")
    ship_to = fields.Many2one('res.partner',string="Ship To")
    outward_id = fields.Many2one('stock.picking',string="Outward No",domain=[('picking_type_id.code','=','outgoing')])
    inward_id = fields.Many2one('stock.picking',string="Inward No",domain=[('picking_type_id.code','=','incoming')])

    @api.onchange('partner_id')
    def _set_bill_to_ship_to(self):
        for rec in self:
            if rec.partner_id and rec.move_type == 'out_refund':
                rec.write({
                    'bill_to':rec.partner_id.id,
                    'ship_to':rec.partner_id.id,
                })


    @api.depends(
        'line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual',
        'line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual_currency',
        'line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual',
        'line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual_currency',
        'line_ids.debit',
        'line_ids.credit',
        'line_ids.currency_id',
        'line_ids.amount_currency',
        'line_ids.amount_residual',
        'line_ids.amount_residual_currency',
        'line_ids.payment_id.state',
        'line_ids.full_reconcile_id')
    def _compute_amount(self):
        for move in self:

            if move.payment_state == 'invoicing_legacy':
                # invoicing_legacy state is set via SQL when setting setting field
                # invoicing_switch_threshold (defined in account_accountant).
                # The only way of going out of this state is through this setting,
                # so we don't recompute it here.
                move.payment_state = move.payment_state
                continue

            total_untaxed = 0.0
            total_untaxed_currency = 0.0
            total_tax = 0.0
            total_tax_currency = 0.0
            total_to_pay = 0.0
            total_residual = 0.0
            total_residual_currency = 0.0
            total = 0.0
            total_currency = 0.0
            currencies = set()

            for line in move.line_ids:
                if line.currency_id and line in move._get_lines_onchange_currency():
                    currencies.add(line.currency_id)

                if move.is_invoice(include_receipts=True):
                    # === Invoices ===

                    if not line.exclude_from_invoice_tab:
                        # Untaxed amount.
                        total_untaxed += line.balance
                        total_untaxed_currency += line.amount_currency
                        total += line.balance
                        total_currency += line.amount_currency
                    elif line.tax_line_id:
                        # Tax amount.
                        total_tax += line.balance
                        total_tax_currency += line.amount_currency
                        total += line.balance
                        total_currency += line.amount_currency
                    elif line.account_id.user_type_id.type in ('receivable', 'payable'):
                        # Residual amount.
                        total_to_pay += line.balance
                        total_residual += line.amount_residual
                        total_residual_currency += line.amount_residual_currency
                else:
                    # === Miscellaneous journal entry ===
                    if line.debit:
                        total += line.balance
                        total_currency += line.amount_currency

            if move.move_type == 'entry' or move.is_outbound():
                sign = 1
            else:
                sign = -1
            move.amount_untaxed = sign * (total_untaxed_currency if len(currencies) == 1 else total_untaxed)
            if move.no_gst == True:
                move.amount_tax = 0.0
            else:
                move.amount_tax = sign * (total_tax_currency if len(currencies) == 1 else total_tax)
            move.amount_total = sign * (total_currency if len(currencies) == 1 else total)
            move.amount_residual = -sign * (total_residual_currency if len(currencies) == 1 else total_residual)
            move.amount_untaxed_signed = -total_untaxed
            move.amount_tax_signed = -total_tax
            move.amount_total_signed = abs(total) if move.move_type == 'entry' else -total
            move.amount_residual_signed = total_residual

            currency = len(currencies) == 1 and currencies.pop() or move.company_id.currency_id

            # Compute 'payment_state'.
            new_pmt_state = 'not_paid' if move.move_type != 'entry' else False

            if move.is_invoice(include_receipts=True) and move.state == 'posted':

                if currency.is_zero(move.amount_residual):
                    reconciled_payments = move._get_reconciled_payments()
                    if not reconciled_payments or all(payment.is_matched for payment in reconciled_payments):
                        new_pmt_state = 'paid'
                    else:
                        new_pmt_state = move._get_invoice_in_payment_state()
                elif currency.compare_amounts(total_to_pay, total_residual) != 0:
                    new_pmt_state = 'partial'

            if new_pmt_state == 'paid' and move.move_type in ('in_invoice', 'out_invoice', 'entry'):
                reverse_type = move.move_type == 'in_invoice' and 'in_refund' or move.move_type == 'out_invoice' and 'out_refund' or 'entry'
                reverse_moves = self.env['account.move'].search(
                    [('reversed_entry_id', '=', move.id), ('state', '=', 'posted'), ('move_type', '=', reverse_type)])

                # We only set 'reversed' state in cas of 1 to 1 full reconciliation with a reverse entry; otherwise, we use the regular 'paid' state
                reverse_moves_full_recs = reverse_moves.mapped('line_ids.full_reconcile_id')
                if reverse_moves_full_recs.mapped('reconciled_line_ids.move_id').filtered(lambda x: x not in (
                        reverse_moves + reverse_moves_full_recs.mapped('exchange_move_id'))) == move:
                    new_pmt_state = 'reversed'

            move.payment_state = new_pmt_state

        # self.ensure_one()
            if move.CGST_SGST == True:
                CS_GST_tax_amount = move.amount_tax / 2
                move.amount_CGST = CS_GST_tax_amount
                move.amount_SGST = CS_GST_tax_amount
            elif move.IGST == True:
                move.amount_IGST = move.amount_tax
            elif move.UTGST == True:
                move.amount_UTGST = move.amount_tax
            else:
                move.amount_tax = 0.00


    amount_CGST = fields.Float(string="CGST", compute="_compute_amount", store=True)
    amount_SGST = fields.Float(string="SGST", compute="_compute_amount", store=True)
    amount_IGST = fields.Float(string="IGST", compute="_compute_amount", store=True)
    amount_UTGST = fields.Float(string="UTGST", compute="_compute_amount", store=True)
    amount_gst_tax = fields.Monetary(string='GST Tax', store=True, readonly=True, compute="_compute_amount")


    def amount_to_text(self, amount, currency):
        convert_amount_in_words = currency.amount_to_text(amount)
        if decimal.Decimal(amount).as_tuple().exponent == 0:
            convert_amount_in_words = convert_amount_in_words.replace(' Cent', ' Only')
        else:
            convert_amount_in_words = convert_amount_in_words.replace(' Cents', ' Only')
        return convert_amount_in_words

    @api.model
    def create(self, vals):
        res = super(CustomAccountInvoice, self).create(vals)
        print(res.id)
        so = self.env['sale.order'].sudo().search_read([('invoice_ids', 'in', [res.id])], limit=1)
        print(res.partner_id)
        if res.no_gst == True and res.CGST_SGST == True or res.IGST == True or res.UTGST == True:
            res.no_gst = False
        data = {'amount_CGST': res.amount_CGST,
                'amount_SGST': res.amount_SGST,
                'amount_IGST': res.amount_IGST,
                'amount_UTGST': res.amount_UTGST,
                'CGST_SGST': res.CGST_SGST,
                'IGST': res.IGST,
                'UTGST': res.UTGST,
                'no_gst': res.no_gst,
                # 'bill_to': res.partner_id,
                # 'ship_to': res.partner_id
                }
        res.write(data)
        return res

    def _write(self, vals):
        res = super(CustomAccountInvoice, self)._write(vals)
        if 'CGST_SGST' in vals.keys():
            if vals['CGST_SGST'] == True:
                self.IGST = self.UTGST = self.no_gst = False

        elif 'IGST' in vals.keys():
            if vals['IGST'] == True:
                self.CGST_SGST = self.UTGST = self.no_gst = False

        elif 'UTGST' in vals.keys():
            if vals['UTGST'] == True:
                self.IGST = self.CGST_SGST = self.no_gst = False

        elif 'no_gst' in vals.keys():
            if vals['no_gst'] == True:
                self.IGST = self.UTGST = self.CGST_SGST = False
        else:
            pass
        return res

    def cal_hsn(self):
        if self.invoice_line_ids:
            hsn_list = []
            for line in self.invoice_line_ids:
                if line.HSN_SAC:
                    hsn_list.append(line.HSN_SAC)
            new_hsn_list = list(set(hsn_list))
            final_hsn_list = []
            for hsn in new_hsn_list:
                qty = 0
                amount = 0
                for line in self.invoice_line_ids:
                    if line.HSN_SAC and line.HSN_SAC == hsn:
                        qty = qty + line.quantity
                        amount = amount + line.price_total
                dict = {
                    'hsn_code':hsn,
                    'quantity':qty,
                    'amount':amount,
                }
                final_hsn_list.append(dict)
            return final_hsn_list
        else:
            return False


class CustomAccountInvoiceLine(models.Model):
    _inherit = "account.move.line"


    @api.depends('product_id', 'move_id.CGST_SGST', 'move_id.IGST', 'move_id.UTGST', 'tax_ids')

    def _compute_gst_percentage(self):
        for order in self:

            total_gst = 0.0
            gst_amount_line = 0.0
            for line in order:
                for tax in line.tax_ids:
                    if tax.amount_type == "group":
                        for child_tax_amount in tax.children_tax_ids:
                            total_gst += child_tax_amount.amount
                        if line.move_id.CGST_SGST == True:
                            CS_GST_percent = total_gst / 2
                            line.invoice_CGST = line.invoice_SGST = CS_GST_percent
                            line.invoice_amount_CGST = line.price_subtotal * line.invoice_CGST/100
                            line.invoice_amount_SGST = line.price_subtotal * line.invoice_SGST/100
                        elif line.move_id.IGST == True:
                            line.invoice_IGST = total_gst
                            line.invoice_amount_IGST = line.price_subtotal * line.invoice_IGST/100
                        elif line.move_id.UTGST == True:
                            line.invoice_UTGST = total_gst
                            line.invoice_amount_UTGST = line.price_subtotal * line.invoice_UTGST/100
                        else:
                            line.invoice_CGST = line.invoice_SGST = 0.00
                            line.invoice_IGST = line.invoice_UTGST = 0.00
                        line.HSN_SAC = line.product_id.HSN_SAC

                    if tax.amount_type == "percent":
                        total_gst += tax.amount
                        if line.move_id.CGST_SGST == True:
                            CS_GST_percent = total_gst / 2
                            line.invoice_CGST = line.invoice_SGST = CS_GST_percent
                            line.invoice_amount_CGST = line.price_subtotal * line.invoice_CGST/100
                            line.invoice_amount_SGST = line.price_subtotal * line.invoice_SGST/100
                        elif line.move_id.IGST == True:
                            line.invoice_IGST = total_gst
                            line.invoice_amount_IGST = line.price_subtotal * line.invoice_IGST/100
                        elif line.move_id.UTGST == True:
                            line.invoice_UTGST = total_gst
                            line.invoice_amount_UTGST = line.price_subtotal * line.invoice_UTGST/100
                        else:
                            line.invoice_CGST = line.invoice_SGST = 0.00
                            line.invoice_IGST = line.invoice_UTGST = 0.00
                        line.HSN_SAC = line.product_id.HSN_SAC
                line.invoice_amount_TAX = line.invoice_CGST + line.invoice_SGST + line.invoice_IGST + line.invoice_UTGST


    invoice_CGST = fields.Float(string="CGST", compute="_compute_gst_percentage", store=True)
    invoice_SGST = fields.Float(string="SGST", compute="_compute_gst_percentage", store=True)
    invoice_IGST = fields.Float(string="IGST", compute="_compute_gst_percentage", store=True)
    invoice_UTGST = fields.Float(string="UTGST", compute="_compute_gst_percentage", store=True)
    HSN_SAC = fields.Char(string="HSN/SAC", compute="_compute_gst_percentage", store=True)
    no_gst = fields.Boolean(string="No GST")

    invoice_amount_CGST = fields.Float(string="CGST Amount", compute="_compute_gst_percentage", store=True)
    invoice_amount_SGST = fields.Float(string="SGST Amount", compute="_compute_gst_percentage", store=True)
    invoice_amount_IGST = fields.Float(string="IGST Amount", compute="_compute_gst_percentage", store=True)
    invoice_amount_UTGST = fields.Float(string="UTGST Amount", compute="_compute_gst_percentage", store=True)

    invoice_amount_TAX = fields.Float(string="Tax Rate", compute='_compute_gst_percentage', store=True)

    @api.depends('product_id', 'move_id.CGST_SGST', 'move_id.IGST', 'move_id.UTGST', 'move_id.no_gst')
    def _set_taxes(self):
        """ Used in on_change to set taxes and price."""
        if self.move_id.type in ('out_invoice', 'out_refund'):
            if self.move_id.no_gst == False:
                taxes = self.product_id.taxes_id or self.account_id.tax_ids
            else:
                taxes = self.env['account.tax']
        else:
            if self.move_id.no_gst == False:
                taxes = self.product_id.supplier_taxes_id or self.account_id.tax_ids
            else:
                taxes = self.env['account.tax']
        # Keep only taxes of the company
        company_id = self.company_id or self.env.user.company_id
        if self.move_id.no_gst == False:
            taxes = taxes.filtered(lambda r: r.company_id == company_id)
        else:
            taxes = self.env['account.tax']
        if self.move_id.no_gst == False:
            self.tax_ids = fp_taxes = self.move_id.fiscal_position_id.map_tax(taxes, self.product_id, self.move_id.partner_id)
        else:
            self.tax_ids = fp_taxes = self.env['account.tax']
        fix_price = self.env['account.tax']._fix_tax_included_price
        if self.move_id.type in ('in_invoice', 'in_refund'):
            prec = self.env['decimal.precision'].precision_get('Product Price')
            if not self.price_unit or float_compare(self.price_unit, self.product_id.standard_price, precision_digits=prec) == 0:
                self.price_unit = fix_price(self.product_id.standard_price, taxes, fp_taxes)
        else:
            self.price_unit = fix_price(self.product_id.lst_price, taxes, fp_taxes)