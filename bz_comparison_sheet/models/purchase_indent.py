# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
##############################################################################
import base64
from io import BytesIO

from odoo import fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools.misc import xlwt
from xlwt import easyxf
from xlwt import easyxf, Formula


class purchase_requisition(models.Model):
    _inherit = 'purchase.requisition'

    comparison_sheet = fields.Binary('Comparison Sheet')

    def get_supplier_name(self, purchase_ids):
        res = []
        for purchase in purchase_ids:
            res.append({'name':purchase.partner_id.name,'email':purchase.partner_id.email,
                        'mobile':purchase.partner_id.mobile})
        return res

    def get_comparison_purchase_price(self, product, purchase, pi_number):
        print ("product=========",product , product.name)
        print ("purchase=========",purchase)
        if product and purchase:
            query = """select price_unit from purchase_order_line \
                          where order_id = %s and product_id = %s and \
                          pi_number = %s """
        params = (purchase.id, product.id , pi_number)
        self.env.cr.execute(query, params)
        result = self.env.cr.dictfetchall()
        price = 0
        if result:
            result = result[0]
            price = result.get('price_unit')
            if purchase.currency_id.id != purchase.company_id.currency_id.id:
                currency_id = purchase.currency_id.with_context(date=purchase.date_order)
                price = currency_id.compute(price, purchase.company_id.currency_id)
        return price

    def action_compair_sheet(self):
        purchase_ids = self.purchase_ids
        if not purchase_ids:
            raise ValidationError(_('Purchase Quotation not created for this indent.'))

        filename = 'comparison_sheet.xls'
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('Comparison Sheet')

        main_header_style = easyxf('font:height 250;pattern: pattern solid, fore_color gray25;'
                                   'align: horiz center, vert center;font: color black; font:bold True;'
                                   "borders: top thin,left thin,right thin,bottom thin")

        header_style = easyxf('font:height 200;pattern: pattern solid, fore_color gray25;'
                              'align: horiz center, vert center;font: color black; font:bold True;'
                              "borders: top thin,left thin,right thin,bottom thin")

        text_left = easyxf('font:height 200; align: horiz left, vert center;' "borders: top thin,left thin,right thin,bottom thin" )
        text_left_bold = easyxf('font:height 200; align: horiz left, vert center;font:bold True;' "borders: top thin,left thin,right thin,bottom thin")
        text_center = easyxf('font:height 200; align: horiz center, vert center;' "borders: top thin,left thin,right thin,bottom thin")

        text_right = easyxf('font:height 200; align: horiz right, vert center;' "borders: top thin,left thin,right thin,bottom thin",
                            num_format_str='0.00' )
        text_right1 = easyxf('font:height 200; align: horiz center, vert center;' "borders: top thin,left thin,right thin,bottom thin",
                             num_format_str='0.00')

#        worksheet.write_merge(0, 0, 0, 6, 'DADASDSD -', main_header_style)

        header_data = str(self.company_id.name or ' ')+'\n'+'COMPARISON SHEET - ' + str(self.name)
        worksheet.write_merge(0, 2, 0, 6, header_data, main_header_style)
        supplier_name = self.get_supplier_name(purchase_ids)
        for i in range(0, (len(supplier_name) * 2) + 4):
            worksheet.col(i).width = 140 * 30
        worksheet.col(6).width = 140 * 40
        
        for i in range(0, 1000):
            worksheet.row(i).height = 350

    

        r = 2
#        worksheet.write_merge(r + 1,r + 1 ,0,3, 'PR Basic Details', header_style)
#        worksheet.write_merge(r + 1,r + 1 ,4,6, ' ', header_style)
#        worksheet.write_merge(r + 1,r + 1 ,7,10, 'RFQ Basic Details', header_style)
#        worksheet.write_merge(r + 1,r + 1 ,11,13, 'Negotiation Outcome', header_style)
        
#        worksheet.write_merge(r + 2,r + 2 ,0,3, 'PRREQUIREMENT TYPE', text_left_bold)
#        worksheet.write_merge(r + 3,r + 3 ,0,3, 'NATURE OF REQUIREMENT', text_left_bold)
#        worksheet.write_merge(r + 4,r + 4 ,0,3, 'PR NO./RC', text_left_bold)
#        worksheet.write_merge(r + 5,r + 5 ,0,3, 'PR DATE', text_left_bold)
#        worksheet.write_merge(r + 6,r + 6 ,0,3, 'TECNICALLY APPROVED BY', text_left_bold)
#        
#        
#        worksheet.write_merge(r + 2,r + 2 ,4,6, '', text_left)
#        worksheet.write_merge(r + 3,r + 3 ,4,6, '', text_left)
#        worksheet.write_merge(r + 4,r + 4 ,4,6, '', text_left)
#        worksheet.write_merge(r + 5,r + 5 ,4,6, '', text_left)
#        worksheet.write_merge(r + 6,r + 6 ,4,6, '', text_left)
        
#        worksheet.write_merge(r + 2,r + 2 ,7,9, 'RFQ Shared to No. of Vendor', text_left_bold)
#        worksheet.write_merge(r + 3,r + 3 ,7,9, 'No. of New Vendor Added', text_left_bold)
#        worksheet.write_merge(r + 4,r + 4 ,7,9, 'Credentials of new bidders shared', text_left_bold)
#        worksheet.write_merge(r + 5,r + 5 ,7,9, 'Consolidated / Split Order', text_left_bold)
#        worksheet.write_merge(r + 6,r + 6 ,7,9, 'Validity of Offer', text_left_bold)
#        
#        worksheet.write(r + 2, 10, " ", text_left)
#        worksheet.write(r + 3, 10, " ", text_left)
#        worksheet.write(r + 4, 10, " ", text_left)
#        worksheet.write(r + 5, 10, " ", text_left)
#        worksheet.write(r + 6, 10, " ", text_left)
#        
#        worksheet.write_merge(r + 2,r + 2 ,11,12, 'AVG. SAVING W.R.TO. LPP-%', text_left_bold)
#        worksheet.write_merge(r + 3,r + 3 ,11,12, 'AVG. SAVING W.R.TO. Intital Quotation-%', text_left_bold)
#        worksheet.write_merge(r + 4,r + 4 ,11,12, 'NAME OF WINNING  VENDOR', text_left_bold)
#        worksheet.write_merge(r + 5,r + 5 ,11,12, 'VALUE OF ORDER(S)', text_left_bold)
#        
#        worksheet.write(r + 2, 13, " ", text_left)
#        worksheet.write(r + 3, 13, " ", text_left)
#        worksheet.write(r + 4, 13, " ", text_left)
#        worksheet.write(r + 5, 13, " ", text_left)
#        worksheet.write(r + 6, 13, " ", text_left)
        
        r = 9 -5
        worksheet.write_merge(r, r + 2, 0, 1, 'Product', header_style)
        worksheet.write_merge(r, r + 2, 2, 2, 'Product Qty', header_style)
        worksheet.write_merge(r, r + 2, 3, 3, 'UOM', header_style)
        worksheet.write_merge(r,r + 2, 4,4, 'LPP', header_style)
        worksheet.write_merge(r,r + 2, 5,5, 'Quoted L0 Rate', header_style)
        worksheet.write_merge(r,r + 2, 6,6, 'Quoted L0 Value', header_style)
        
        c = 7
        for sup in supplier_name:
            sup_info = str(sup.get('name'))+'\n'+'E : '+str(sup.get('email'))+'\n'+'M : '+str(sup.get('mobile'))
            worksheet.write_merge(r, r+1, c, c + 1, sup_info, header_style)
            worksheet.write(r + 2, c, 'Price', header_style)
            worksheet.write(r + 2, c + 1, 'Value', header_style)
            c += 2
        r = 12-5
        for line in self.line_ids:
            worksheet.write_merge(r, r, 0, 1, line.product_id.display_name or '', text_left)
            worksheet.write(r, 2, line.product_qty, text_right1)
            worksheet.write(r, 3, line.product_uom_id.name, text_center)
            c = 7
            for purchase in purchase_ids:
                print ("line.product_id=======",line.product_id ,line.pi_number )
                price = self.get_comparison_purchase_price(line.product_id, purchase, line.pi_number or "005")
                t_price = price
                if t_price == 0:
                    t_price = ' '
                worksheet.write(r, c, t_price, text_right)
                c += 1
                value = price * line.product_qty
                t_value = value
                if t_value == 0:
                    t_value = ' '
                worksheet.write(r, c, t_value, text_right)
                c += 1
            r += 1
        c = 7
        number_alphabet = {1: 'A', 2: 'b', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H', 9: 'I', 10 : 'J', 11: 'K', 12: 'L', 13: 'M', 14: 'N', 15: 'O', 16: 'P', 17: 'Q', 18: 'R', 19: 'S', 20: 'T', 21: 'U', 22: 'V', 23: 'W', 24: 'X', 25: 'Y', 26: 'Z'}
        for purchase in purchase_ids:
            c += 1
            alp_sub = c+1
            alp_one = number_alphabet.get(alp_sub)
            packing_forwarding_charges = 0
            if purchase.packing_forwarding == 'fixed':
                packing_forwarding_charges = purchase.packing_forwarding_charges
            if purchase.packing_forwarding == 'percentage':
                packing_forwarding_charges = (purchase.amount_untaxed * purchase.packing_forwarding_charges) /100
            
            freight_charges = 0
            if purchase.freight == 'fixed':
                freight_charges = purchase.freight_charges
            if purchase.freight == 'percentage':
                freight_charges = (purchase.amount_untaxed * purchase.freight_charges) /100
                
            other_charges = 0
            if purchase.freight == 'fixed':
                other_charges = purchase.other_charges
            if purchase.other == 'percentage':
                other_charges = (purchase.amount_untaxed * purchase.other_charges) /100
                
            f = 'SUM('+str(alp_one)+str(8)+':'+str(alp_one)+str(r)+')'
            payment_term = purchase.payment_term_id and purchase.payment_term_id.name or ' ' 
            worksheet.write(r,c, Formula(f), text_right)
            worksheet.write(r+2,c-1, "Packing & Forwarding - "+str(purchase.packing_forwarding), text_right)
            worksheet.write(r+2,c, packing_forwarding_charges, text_right)
            worksheet.write(r+3,c-1, "Freight - "+str(purchase.freight), text_right)
            worksheet.write(r+3,c, freight_charges, text_right)
            worksheet.write(r+4,c-1, "Other Charges - "+str(purchase.other), text_right)
            worksheet.write(r+4,c, other_charges, text_right)
            
            total_charges_formula = 'SUM('+str(alp_one)+str(r+1)+':'+str(alp_one)+str(r+5)+')'
            worksheet.write(r+5,c, Formula(total_charges_formula), text_right)
            
            worksheet.write(r+6,c,purchase.amount_tax , text_right)
            
            worksheet.write(r+8,c,purchase.landed_cost_lc , text_right)
            worksheet.write(r+9,c,purchase.landed_cost_lc_gst , text_right)
            
            worksheet.write_merge(r+10,r+10, c-1,c, purchase.credentials or ' ', text_right)
            
            worksheet.write_merge(r+11,r+11, c-1,c, purchase.technical_rating or ' ', text_right)
            worksheet.write_merge(r+12,r+12, c-1,c, purchase.commercial_rating or ' ', text_right)
            worksheet.write_merge(r+13,r+13, c-1,c, purchase.final_recommendtation or ' ', text_right)
            worksheet.write_merge(r+14,r+14, c-1,c, purchase.any_other or ' ', text_right)
            
            worksheet.write_merge(r+15,r+15, c-1,c, purchase.delivery or ' ', text_right)
            worksheet.write_merge(r+16,r+16, c-1,c, purchase.ld_clause or ' ', text_right)
            worksheet.write_merge(r+17,r+17, c-1,c, purchase.warranty or ' ', text_right)
            
            worksheet.write_merge(r+19,r+19, c-1,c, payment_term or ' ' , text_right) 
            
            
            c += 1
            
        
        worksheet.write_merge(r,r, 0,1 ,"TOTAL PRIC ", text_left_bold)
        worksheet.write_merge(r+1,r+1, 0,1, "", text_left_bold)
        worksheet.write_merge(r+2,r+2, 0,1, "Packing & Forwarding (flat/%)", text_left_bold)
        worksheet.write_merge(r+3,r+3, 0,1, "Freight (flat/%)", text_left_bold)
        worksheet.write_merge(r+4,r+4, 0,1, "Other Charges (flat/%)", text_left_bold)
        worksheet.write_merge(r+5,r+5, 0,1, "Total with additional Charges", text_left_bold)
        worksheet.write_merge(r+6,r+6, 0,1, "GST", text_left_bold)
        worksheet.write_merge(r+7,r+7, 0,1, "Other taxes/Duties/Levieses  (flat/%)", text_left_bold)
        worksheet.write_merge(r+8,r+8, 0,1, "Landed Cost (LC) in Rs", text_left_bold)
        worksheet.write_merge(r+9,r+9, 0,1, "Landed Cost (LC) net off GST -in Rs  ", text_left_bold)
        
        
        
        
        
        
#        worksheet.write_merge(r+10,r+10, 0,1, "PERFORMANCE  ", text_left_bold)
        worksheet.write_merge(r+10,r+10, 0,1, "CREDENTIALS ", text_left_bold)
        worksheet.write_merge(r+11,r+11, 0,1, "Technical rating ", text_left_bold)
        worksheet.write_merge(r+12,r+12, 0,1, "Commercial Rating ", text_left_bold)
        
        worksheet.write_merge(r+13,r+13, 0,1, "Final recommendtation ", text_left_bold)
        worksheet.write_merge(r+14,r+14, 0,1, "Any Other ", text_left_bold)
        worksheet.write_merge(r+15,r+15, 0,1, "DELIVERY  ", text_left_bold)
        worksheet.write_merge(r+16,r+16, 0,1, "LD CLAUSE  ", text_left_bold)
#        worksheet.write_merge(r+19,r+19, 0,1, "GST", text_left_bold)
#        worksheet.write_merge(r+20,r+20, 0,1, "TCS", text_left_bold)
        worksheet.write_merge(r+17,r+17, 0,1, "WARRANTY", text_left_bold)
        worksheet.write_merge(r+18,r+18, 0,1, "Validity of Quotation", text_left_bold)
        worksheet.write_merge(r+19,r+19, 0,1, "PAYMENT TERMS ", text_left_bold)

        fp = BytesIO()
        workbook.save(fp)
        fp.seek(0)
        comparison_sheet = base64.encodestring(fp.read())
        fp.close()
        self.write({'comparison_sheet': comparison_sheet})
        active_id = self.ids[0]
        url = ('web/content/?models=purchase.requisition&download=true&field=comparison_sheet&id=%s&filename=%s' % (active_id, filename))
        if self.comparison_sheet:
            return {'type': 'ir.actions.act_url',
                    'url': url,
                    'target': 'new'}
                    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
