from odoo import models, fields, _, api
from odoo.tools.misc import formatLang, get_lang
from odoo.exceptions import AccessError, UserError, ValidationError
from datetime import datetime

class SoBlanket(models.Model):
    _name = 'so.blanket'
    _description = "SO Blanket"
    _rec_name = "name"

    def unlink(self):
        if self.state in ['open', 'expired']:
            raise ValidationError(_('You can not delete a record that is in Open or Expired State. '))
        return super(SoBlanket, self).unlink()

    @api.model
    def _blanket_order_set_expired(self):
        blanket_ids = self.env['so.blanket'].search([('expiry_date', '=', datetime.today())])
        if blanket_ids:
            for req in blanket_ids:
                req.state = 'expired'

    @api.model
    def create(self, vals):
        if self.state == 'expired':
            raise ValidationError(_('Blanket Order Expired.'))
        if 'company_id' in vals:
            self = self.with_company(vals['company_id'])
        if vals.get('name', _('New')) == _('New'):
            seq_date = None
            if 'date_order' in vals:
                seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.to_datetime(vals['date_order']))
            vals['name'] = self.env['ir.sequence'].next_by_code('so.blanket', sequence_date=seq_date) or _('New')

        # Makes sure partner_invoice_id', 'partner_shipping_id' and 'pricelist_id' are defined
        if any(f not in vals for f in ['partner_invoice_id', 'partner_shipping_id', 'pricelist_id']):
            partner = self.env['res.partner'].browse(vals.get('partner_id'))
            addr = partner.address_get(['delivery', 'invoice'])
            vals['partner_invoice_id'] = vals.setdefault('partner_invoice_id', addr['invoice'])
            vals['partner_shipping_id'] = vals.setdefault('partner_shipping_id', addr['delivery'])
            vals['pricelist_id'] = vals.setdefault('pricelist_id', partner.property_product_pricelist.id)
        result = super(SoBlanket, self).create(vals)
        return result

    def action_view_quotation(self):
        self.ensure_one()

        # Create action.
        action = {
            'name': _('Quotations'),
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
        }
        reverse_entries = self.env['sale.order'].search([('bk_ref_id', '=', self.id)])
        if len(reverse_entries) == 1:
            action.update({
                'view_mode': 'form',
                'res_id': reverse_entries.id,
            })
        else:
            action.update({
                'view_mode': 'tree,form',
                'domain': [('id', 'in', reverse_entries.ids)],
            })
        return action

    def action_state_open(self):
        if self.state == 'expired':
            raise ValidationError(_('Blanket Order Expired.'))
        self.state = 'open'

    @api.depends('quotation_count')
    def _compute_blanket_ids(self):
        self.quotation_count = 0
        linked_so = self.env['sale.order'].search([('bk_ref_id', '=', self.id)])
        is_present = len(linked_so)
        if is_present:
            self.quotation_count = len(linked_so)

    def action_create_quotation(self):
        create_line = True
        if self.user_id:
            user_id = self.user_id.id
        if self.payment_term_id:
            payment_term_id = self.payment_term_id.id
        if self.state == 'expired':
            raise ValidationError(_('Blanket Order Expired.'))
        qty = 0.0
        new_wizard = self.env['create.sale.quotation'].create({})
        if self.order_line:
            for req in self.order_line:
                quotation_obj = self.env['sale.order'].search([('bk_ref_id', '=', self.id)])
                if req.remaining_qty == 0.0 and quotation_obj:
                    create_line = False
                if req.remaining_qty:
                    qty = req.remaining_qty
                else:
                    qty = req.product_uom_qty
                if create_line:
                    new_wizard.write({
                        'bk_ref_id': self.id,
                        'user_id': user_id,
                        'payment_term_id': payment_term_id,
                        'name': self.name,
                        'partner_id': self.partner_id.id,
                        'quotation_line_ids': [(0, 0, {'product_id': req.product_id.id,
                                                       'partner_id': self.partner_id.id,
                                                       'remaining_qty': qty,
                                                       'new_quotation_qty': 0.0,
                                                       'tax_id': [(6, 0, req.tax_id.ids)],
                                                       'bk_ref_id': self.id,
                                                       })]

                    })
        view_id = self.env.ref('bz_blanket_sale_order.create_sale_quotation_form').id

        return {
            'type': 'ir.actions.act_window',
            'name': _('Create Sale Quotation'),
            'view_mode': 'form',
            'res_model': 'create.sale.quotation',
            'target': 'new',
            'res_id': new_wizard.id,
            'views': [[view_id, 'form']],
        }

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        """
        Update the following fields when the partner is changed:
        - Pricelist
        - Payment terms
        - Invoice address
        - Delivery address
        - Sales Team
        """
        if not self.partner_id:
            self.update({
                'partner_invoice_id': False,
                'partner_shipping_id': False,
                'fiscal_position_id': False,
            })
            return

        self = self.with_company(self.company_id)

        addr = self.partner_id.address_get(['delivery', 'invoice'])
        partner_user = self.partner_id.user_id or self.partner_id.commercial_partner_id.user_id
        values = {
            'pricelist_id': self.partner_id.property_product_pricelist and self.partner_id.property_product_pricelist.id or False,
            'payment_term_id': self.partner_id.property_payment_term_id and self.partner_id.property_payment_term_id.id or False,
            'partner_invoice_id': addr['invoice'],
            'partner_shipping_id': addr['delivery'],
        }
        user_id = partner_user.id
        if not self.env.context.get('not_self_saleperson'):
            user_id = user_id or self.env.context.get('default_user_id', self.env.uid)
        if user_id and self.user_id.id != user_id:
            values['user_id'] = user_id

        if self.env['ir.config_parameter'].sudo().get_param(
                'account.use_invoice_terms') and self.env.company.invoice_terms:
            values['note'] = self.with_context(lang=self.partner_id.lang).env.company.invoice_terms
        self.update(values)

    @api.onchange('fiscal_position_id')
    def _compute_tax_id(self):
        """
        Trigger the recompute of the taxes if the fiscal position is changed on the SO.
        """
        for order in self:
            order.order_line._compute_tax_id()

    def action_cancel(self):
        return self.write({'state': 'canceled'})

    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                       states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    partner_id = fields.Many2one(
        'res.partner', string='Customer',
        required=True, change_default=True, index=True, tracking=1, states={'open': [('readonly', True)]})
    payment_term_id = fields.Many2one(
        'account.payment.term', string='Payment Terms', states={'open': [('readonly', True)]})
    expiry_date = fields.Date('Expiry Date')
    partner_invoice_id = fields.Many2one(
        'res.partner', string='Invoice Address', states={'open': [('readonly', True)]})
    partner_shipping_id = fields.Many2one(
        'res.partner', string='Delivery Address', states={'open': [('readonly', True)]})
    pricelist_id = fields.Many2one(
        'product.pricelist', string='Pricelist', tracking=1, required=True, states={'open': [('readonly', True)]})
    order_line = fields.One2many('so.blanket.line', 'order_id', string='Order Lines', copy=True,auto_join=True, states={'open': [('readonly', True)]})

    company_id = fields.Many2one('res.company', 'Company', required=True, index=True,
                                 default=lambda self: self.env.company)
    fiscal_position_id = fields.Many2one(
        'account.fiscal.position', string='Fiscal Position')
    currency_id = fields.Many2one(related='pricelist_id.currency_id', depends=["pricelist_id"], store=True)
    user_id = fields.Many2one(
        'res.users', string='Salesperson', index=True, tracking=2, default=lambda self: self.env.user,
        domain=lambda self: [('groups_id', 'in', self.env.ref('sales_team.group_sale_salesman').id)])
    state = fields.Selection([
        ('draft', 'New'),
        ('open', 'Open'),
        ('expired', 'Expired'),
        ('canceled', 'Canceled')
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
    quotation_count = fields.Integer(string='Quotation Orders', compute='_compute_blanket_ids')


class SoBlanketLine(models.Model):
    _name = 'so.blanket.line'
    _description = 'Sales Order Blanket Line'

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty,
                                            product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })
            if self.env.context.get('import_file', False) and not self.env.user.user_has_groups(
                    'account.group_account_manager'):
                line.tax_id.invalidate_cache(['invoice_repartition_line_ids'], [line.tax_id.id])


    def _get_invoice_qty(self):
        quotation_line_ids = self.env['sale.order.line'].search([('bk_ref_id', '=', self.order_id.id)])
        if quotation_line_ids:
            for blanket_line in self.order_id.order_line:
                for so_line in quotation_line_ids:
                    if blanket_line.product_id.id == so_line.product_id.id:
                        blanket_line.qty_invoiced += so_line.qty_invoiced
        else:
            for blanket_line in self.order_id.order_line:
                blanket_line.qty_invoiced = 0.0


    order_id = fields.Many2one('so.blanket', string='Order Reference', required=True, ondelete='cascade', index=True,
                               copy=False)
    name = fields.Text(string='Description')
    product_id = fields.Many2one('product.product', string='Product', domain="[('sale_ok', '=', True)]")
    product_uom_qty = fields.Float(string='Quantity', digits='Product Unit of Measure', required=True, default=1.0)
    remaining_qty = fields.Float(string='Remaining Quantity', digits='Product Unit of Measure')
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure', domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id', readonly=True)
    tax_id = fields.Many2many('account.tax', string='Taxes', context={'active_test': False})
    product_custom_attribute_value_ids = fields.One2many('product.attribute.custom.value', 'blanket_order_line_id',
                                                         string="Custom Values", copy=True)
    product_no_variant_attribute_value_ids = fields.Many2many('product.template.attribute.value', string="Extra Values",
                                                              ondelete='restrict')
    company_id = fields.Many2one(related='order_id.company_id', string='Company', store=True, readonly=True, index=True)
    order_partner_id = fields.Many2one(related='order_id.partner_id', store=True, string='Customer', readonly=False)
    currency_id = fields.Many2one(related='order_id.currency_id', depends=['order_id.currency_id'], store=True,
                                  string='Currency', readonly=True)
    price_unit = fields.Float('Unit Price', required=True, digits='Product Price', default=0.0)
    price_subtotal = fields.Monetary(compute='_compute_amount', string='Subtotal', readonly=True, store=True)
    price_tax = fields.Float(compute='_compute_amount', string='Total Tax', readonly=True, store=True)
    price_total = fields.Monetary(compute='_compute_amount', string='Total', readonly=True, store=True)
    discount = fields.Float(string='Discount (%)', digits='Discount', default=0.0)
    qty_invoiced = fields.Float(
        compute='_get_invoice_qty', string='Invoiced Quantity',
        digits='Product Unit of Measure')

    @api.onchange('product_id')
    def product_id_change(self):
        if not self.product_id:
            return
        valid_values = self.product_id.product_tmpl_id.valid_product_template_attribute_line_ids.product_template_value_ids
        # remove the is_custom values that don't belong to this template
        for pacv in self.product_custom_attribute_value_ids:
            if pacv.custom_product_template_attribute_value_id not in valid_values:
                self.product_custom_attribute_value_ids -= pacv

        # remove the no_variant attributes that don't belong to this template
        for ptav in self.product_no_variant_attribute_value_ids:
            if ptav._origin not in valid_values:
                self.product_no_variant_attribute_value_ids -= ptav

        vals = {}
        if not self.product_uom or (self.product_id.uom_id.id != self.product_uom.id):
            vals['product_uom'] = self.product_id.uom_id
            vals['product_uom_qty'] = self.product_uom_qty or 1.0

        product = self.product_id.with_context(
            lang=get_lang(self.env, self.order_id.partner_id.lang).code,
            partner=self.order_id.partner_id,
            quantity=vals.get('product_uom_qty') or self.product_uom_qty,
            # date=self.order_id.date_order,
            pricelist=self.order_id.pricelist_id.id,
            uom=self.product_uom.id
        )

        vals.update(name=self.get_sale_order_line_multiline_description_sale(product))

        self._compute_tax_id()

        if self.order_id.pricelist_id and self.order_id.partner_id:
            vals['price_unit'] = self.env['account.tax']._fix_tax_included_price_company(
                self._get_display_price(product), product.taxes_id, self.tax_id, self.company_id)
        self.update(vals)

        title = False
        message = False
        result = {}
        warning = {}
        if product.sale_line_warn != 'no-message':
            title = _("Warning for %s", product.name)
            message = product.sale_line_warn_msg
            warning['title'] = title
            warning['message'] = message
            result = {'warning': warning}
            if product.sale_line_warn == 'block':
                self.product_id = False

        return result

    def get_sale_order_line_multiline_description_sale(self, product):
        """ Compute a default multiline description for this sales order line.

        In most cases the product description is enough but sometimes we need to append information that only
        exists on the sale order line itself.
        e.g:
        - custom attributes and attributes that don't create variants, both introduced by the "product configurator"
        - in event_sale we need to know specifically the sales order line as well as the product to generate the name:
          the product is not sufficient because we also need to know the event_id and the event_ticket_id (both which belong to the sale order line).
        """
        return product.get_product_multiline_description_sale() + self._get_sale_order_line_multiline_description_variants()

    def _get_sale_order_line_multiline_description_variants(self):
        """When using no_variant attributes or is_custom values, the product
        itself is not sufficient to create the description: we need to add
        information about those special attributes and values.

        :return: the description related to special variant attributes/values
        :rtype: string
        """
        if not self.product_custom_attribute_value_ids and not self.product_no_variant_attribute_value_ids:
            return ""

        name = "\n"

        custom_ptavs = self.product_custom_attribute_value_ids.custom_product_template_attribute_value_id
        no_variant_ptavs = self.product_no_variant_attribute_value_ids._origin

        # display the no_variant attributes, except those that are also
        # displayed by a custom (avoid duplicate description)
        for ptav in (no_variant_ptavs - custom_ptavs):
            name += "\n" + ptav.with_context(lang=self.order_id.partner_id.lang).display_name

        # Sort the values according to _order settings, because it doesn't work for virtual records in onchange
        custom_values = sorted(self.product_custom_attribute_value_ids, key=lambda r: (r.custom_product_template_attribute_value_id.id, r.id))
        # display the is_custom values
        for pacv in custom_values:
            name += "\n" + pacv.with_context(lang=self.order_id.partner_id.lang).display_name

        return name

    def _compute_tax_id(self):
        for line in self:
            line = line.with_company(line.company_id)
            fpos = line.order_id.fiscal_position_id or line.order_id.fiscal_position_id.get_fiscal_position(line.order_partner_id.id)
            # If company_id is set, always filter taxes by the company
            taxes = line.product_id.taxes_id.filtered(lambda t: t.company_id == line.env.company)
            line.tax_id = fpos.map_tax(taxes, line.product_id, line.order_id.partner_shipping_id)

    def _get_display_price(self, product):
        # TO DO: move me in master/saas-16 on sale.order
        # awa: don't know if it's still the case since we need the "product_no_variant_attribute_value_ids" field now
        # to be able to compute the full price

        # it is possible that a no_variant attribute is still in a variant if
        # the type of the attribute has been changed after creation.
        no_variant_attributes_price_extra = [
            ptav.price_extra for ptav in self.product_no_variant_attribute_value_ids.filtered(
                lambda ptav:
                    ptav.price_extra and
                    ptav not in product.product_template_attribute_value_ids
            )
        ]
        if no_variant_attributes_price_extra:
            product = product.with_context(
                no_variant_attributes_price_extra=tuple(no_variant_attributes_price_extra)
            )

        if self.order_id.pricelist_id.discount_policy == 'with_discount':
            return product.with_context(pricelist=self.order_id.pricelist_id.id, uom=self.product_uom.id).price
        product_context = dict(self.env.context, partner_id=self.order_id.partner_id.id, date=self.order_id.date_order, uom=self.product_uom.id)

        final_price, rule_id = self.order_id.pricelist_id.with_context(product_context).get_product_price_rule(product or self.product_id, self.product_uom_qty or 1.0, self.order_id.partner_id)
        base_price, currency = self.with_context(product_context)._get_real_price_currency(product, rule_id, self.product_uom_qty, self.product_uom, self.order_id.pricelist_id.id)
        if currency != self.order_id.pricelist_id.currency_id:
            base_price = currency._convert(
                base_price, self.order_id.pricelist_id.currency_id,
                self.order_id.company_id or self.env.company, self.order_id.date_order or fields.Date.today())
        # negative discounts (= surcharge) are included in the display price
        return max(base_price, final_price)

class ProductAttributeCustomValue(models.Model):
    _inherit = "product.attribute.custom.value"

    blanket_order_line_id = fields.Many2one('so.blanket.line', string="Blanket Order Line", required=True, ondelete='cascade')

    _sql_constraints = [
        ('sol_custom_value_unique', 'unique(custom_product_template_attribute_value_id, blanket_order_line_id)',
         "Only one Custom Value is allowed per Attribute Value per Sales Order Line.")
    ]