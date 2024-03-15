from odoo import models

class OrderExecutionXlsx(models.AbstractModel):
    _name = 'report.bz_order_execution.report_order_execution_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        sheet = workbook.add_worksheet('Order Execution Report')
        bold = workbook.add_format({'bold': True, 'align': 'center'})
        header0 = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': '#2D3E15'})
        header1 = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': 'green'})
        header2 = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': '#749449'})
        header3 = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': '#842613'})
        header4 = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': '#BB3216'})
        header5 = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': '#E59281'})
        header6 = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': '#815406'})
        header7 = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': '#A96E07'})
        header8 = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': '#DCC9A9'})
        header9 = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': '#162639'})
        header10 = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': '#478CDE'})
        header11 = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': '#A7BFDC'})
        header12 = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': '#340F3E'})
        header13 = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': '#84249E'})
        header14 = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': '#BDA9C2'})
        header15 = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': '#785513'})
        header16 = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': '#AD7E24'})
        header17 = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': '#CFBC96'})
        header18 = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': '#381D48'})
        header19 = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': '#A898B1'})
        header20 = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': '#147B70'})
        date_style = workbook.add_format({'text_wrap': True, 'num_format': 'dd-mm-yyyy', 'bold': True, 'align': 'center'})
        sheet.set_column('A:BL', 15)
        sheet.merge_range('A1:F1', 'DOCUMENTATION', header0)
        sheet.merge_range('A2:F2', 'ORDER CONFIRMATION', header1)
        sheet.merge_range('A3:D3', 'PI ISSUED', header2)
        sheet.write(2, 4, '', header2)
        sheet.write(2, 5, 'PO FROM BUYER', header2)
        sheet.write(3, 0, 'S.No', header2)
        sheet.write(3, 1, 'Booked BY', header2)
        sheet.write(3, 2, 'PI NUMBER', header2)
        sheet.write(3, 3, 'DATE', header2)
        sheet.write(3, 4, 'PROCESSOR', header2)
        sheet.write(3, 5, 'PO NUMBER', header2)

        sheet.merge_range('G1:O1', 'MARKETING', header3)
        sheet.merge_range('G2:O2', 'ORDER DETAILS', header4)
        sheet.merge_range('G3:O3', 'PURCHASE ORDER', header5)
        sheet.write(3, 6, 'PO DATE', header5)
        sheet.write(3, 7, 'CONSIGNEE', header5)
        sheet.write(3, 8, 'TYPE', header5)
        sheet.write(3, 9, 'ASSORTMENT', header5)
        sheet.write(3, 10, '', header5)
        sheet.write(3, 11, 'PACKING INSTRUCTIONS', header5)
        sheet.write(3, 12, 'LOADING INSTRUCTIONS', header5)
        sheet.write(3, 13, 'PAYMENT TERMS', header5)
        sheet.write(3, 14, 'SHIPMENT DATE', header5)

        sheet.merge_range('P1:X1', 'QA DEPARTMENT', header6)
        sheet.merge_range('P2:Q2', 'CODELIST', header7)
        sheet.merge_range('R2:X2', 'TEST REPORTS', header7)
        sheet.write(2, 15, 'REQUEST', header8)
        sheet.write(2, 16, 'ISSUED', header8)
        sheet.write(2, 17, 'BUYER APPROVAL', header8)
        sheet.write(2, 18, 'THIRD PARTY LAB', header8)
        sheet.write(2, 19, 'TEST REPORTS', header8)
        sheet.write(2, 20, 'EIA SAMPLE PAYMENT', header8)
        sheet.write(2, 21, 'LETTER FOR DRAWING SAMPLE', header8)
        sheet.write(2, 22, 'ARRIVAL OF EIA TO COLLECT SAMPLE', header8)
        sheet.write(2, 23, 'TEST RESULTS', header8)
        sheet.write(3, 15, 'DATE', header8)
        sheet.write(3, 16, 'DATE', header8)
        sheet.write(3, 17, 'DATE', header8)
        sheet.write(3, 18, 'DATE', header8)
        sheet.write(3, 19, 'DATE', header8)
        sheet.write(3, 20, 'DATE', header8)
        sheet.write(3, 21, 'DATE', header8)
        sheet.write(3, 22, 'DATE', header8)
        sheet.write(3, 23, 'DATE', header8)

        sheet.merge_range('Y1:AA1', 'DOCUMENTATION', header9)
        sheet.merge_range('Y2:AA2', 'LABEL & HEADER CARDS', header10)
        sheet.write(2, 24, 'DRAFT FROM BUYER', header11)
        sheet.write(2, 25, 'DRAFT FROM PRINTER', header11)
        sheet.write(2, 26, 'BUYER APPROVAL', header11)
        sheet.write(3, 24, 'DATE', header11)
        sheet.write(3, 25, 'DATE', header11)
        sheet.write(3, 26, 'DATE', header11)

        sheet.merge_range('AB1:AE1', 'COMMERICAL', header12)
        sheet.merge_range('AB2:AE2', 'PACKING MATERIAL', header13)
        sheet.write(2, 27, 'LABELS/HEADER CARDS', header14)
        sheet.write(2, 28, 'POLYTENE', header14)
        sheet.write(2, 29, 'CHEMICAL', header14)
        sheet.write(2, 30, 'CARTON', header14)
        sheet.write(3, 27, 'DATE', header14)
        sheet.write(3, 28, 'DATE', header14)
        sheet.write(3, 29, 'DATE', header14)
        sheet.write(3, 30, 'DATE', header14)

        sheet.write(0, 31, 'MARKETING', header6)
        sheet.merge_range('AG1:AH1', 'QA', header6)
        sheet.merge_range('AF2:AH2', 'QUALITY INSPECTION', header7)
        sheet.write(2, 31, 'BUYER ARRIVAL', header8)
        sheet.write(2, 32, 'SELF INSPECTION', header8)
        sheet.write(2, 33, 'BUYER INSPECTION', header8)
        sheet.write(3, 31, 'DATE', header8)
        sheet.write(3, 32, 'DATE', header8)
        sheet.write(3, 33, 'DATE', header8)

        sheet.merge_range('AI1:AK1', 'PRODUCTION', header0)
        sheet.merge_range('AI2:AK2', 'PRODUCTION STATUS', header1)
        sheet.write(2, 34, 'READINESS OF CARGO', header2)
        sheet.write(2, 35, 'FINAL PACKED', header2)
        sheet.write(2, 36, 'CONTAINER LOADING', header2)
        sheet.write(3, 34, 'STATUS', header2)
        sheet.write(3, 35, 'STATUS', header2)
        sheet.write(3, 36, 'DATE', header2)

        sheet.merge_range('AL1:AM1', 'QA', header6)
        sheet.merge_range('AL2:AM2', 'CERTIFICATES', header7)
        sheet.write(2, 37, 'HEALTH CERTIFICATE', header8)
        sheet.write(2, 38, 'CFE CERTIFICATE', header8)
        sheet.write(3, 37, 'DATE', header8)
        sheet.write(3, 38, 'DATE', header8)

        sheet.merge_range('AN1:AT1', 'EXPORT', header15)
        sheet.merge_range('AN2:AP2', 'APPROVAL FOR LOADING', header16)
        sheet.merge_range('AQ2:AT2', 'CONTAINER', header16)
        sheet.merge_range('AN3:AO3', 'BUYER APPROVAL', header17)
        sheet.write(2, 41, 'PAYMENT', header17)
        sheet.write(2, 42, 'CONTAINER LIFTED', header17)
        sheet.write(2, 43, 'CONTAINER ARRIVAL', header17)
        sheet.write(2, 44, 'INVOICE NUMBER', header17)
        sheet.write(2, 45, 'DISPATCH FROM FACTORY', header17)
        sheet.write(3, 39, 'ONLINE', header17)
        sheet.write(3, 40, 'CONTAINER', header17)
        sheet.write(3, 41, 'LC/ADV', header17)
        sheet.write(3, 42, 'DATE', header17)
        sheet.write(3, 43, 'DATE', header17)
        sheet.write(3, 44, '', header17)
        sheet.write(3, 45, 'DATE', header17)

        sheet.merge_range('AU1:AY1', 'FINANCE', header18)
        sheet.write(1, 46, 'PAYMENT TERMS', header19)
        sheet.write(1, 47, 'ADV PAYMENT', header19)
        sheet.write(1, 48, 'FUNDS RECEIVED', header19)
        sheet.write(1, 49, 'DUTY DRAW BACK RECEIPT', header19)
        sheet.write(1, 50, 'RODTEP SCRIPT GENERATION', header19)
        sheet.write(2, 46, '', header19)
        sheet.write(2, 47, '', header19)
        sheet.write(2, 48, '', header19)
        sheet.write(2, 49, '', header19)
        sheet.write(2, 50, '', header19)
        sheet.write(3, 46, '', header19)
        sheet.write(3, 47, 'DATE', header19)
        sheet.write(3, 48, 'DATE', header19)
        sheet.write(3, 49, 'DATE', header19)
        sheet.write(3, 50, 'DATE', header19)

        sheet.merge_range('AZ1:BC1', 'ORDER EXECUTION TIME', header20)
        sheet.merge_range('BD1:BG1', 'SHIPMENT TO FUND TRANSFER TIME', header20)
        sheet.merge_range('AZ2:BG2', '', header20)
        sheet.merge_range('AZ3:BG3', '', header20)
        sheet.merge_range('AZ4:BG4', '', header20)

        sheet.write(0, 59, 'Remarks', bold)
        sheet.write(0, 60, 'Reason', bold)
        sheet.write(0, 61, 'AGENT COMMISION', bold)
        sheet.write(0, 62, 'PO TO PRODUCTION TIMING', bold)
        sheet.write(0, 63, 'NAME OF THE CONSCERN PERSONS', bold)

        # Body Section
        active_ids = data['context']['active_ids']
        if active_ids:
            row = 4
            col = 0
            sec = 1
            for active_id in active_ids:
                record_set = self.env['order.execution'].browse(active_id)
                if record_set:
                    sheet.write(row, col, sec, bold)
                    sheet.write(row, col + 1, record_set.booked_by or '', bold)
                    sheet.write(row, col + 2, record_set.pi_number or '', bold)
                    sheet.write(row, col + 3, record_set.order_confirmation_date or '', bold)
                    sheet.write(row, col + 4, record_set.processor or '', bold)
                    sheet.write(row, col + 5, record_set.po_number or '', bold)

                    sheet.write(row, col + 6, record_set.po_date or '', bold)
                    sheet.write(row, col + 7, record_set.consignee or '', bold)
                    sheet.write(row, col + 8, record_set.order_detail_type or '', bold)
                    sheet.write(row, col + 9, record_set.order_detail_assortment or '', bold)
                    sheet.write(row, col + 11, record_set.packing_instructions or '', bold)
                    sheet.write(row, col + 12, record_set.loading_instructions or '', bold)
                    sheet.write(row, col + 13, record_set.payment_terms or '', bold)
                    sheet.write(row, col + 14, record_set.shipment_date or '', date_style)

                    sheet.write(row, col + 15, record_set.request_date or '', date_style)
                    sheet.write(row, col + 16, record_set.issued_date or '', date_style)
                    sheet.write(row, col + 17, record_set.buyer_approval_date or '', bold)
                    sheet.write(row, col + 18, record_set.third_party_lab or '', date_style)
                    sheet.write(row, col + 19, record_set.test_report or '', date_style)
                    sheet.write(row, col + 20, record_set.eia_sample_payment or '', date_style)
                    sheet.write(row, col + 21, record_set.letter_for_drawing_sample or '', date_style)
                    sheet.write(row, col + 22, record_set.arrival_eia_collect_sample or '', date_style)
                    sheet.write(row, col + 23, record_set.test_results or '', date_style)

                    sheet.write(row, col + 24, record_set.draft_from_buyer or '', bold)
                    sheet.write(row, col + 25, record_set.draft_from_printer or '', bold)
                    sheet.write(row, col + 26, record_set.buyer_approval or '', bold)

                    sheet.write(row, col + 27, record_set.labels_header_cards or '', bold)
                    sheet.write(row, col + 28, record_set.polythene or '', bold)
                    sheet.write(row, col + 29, record_set.chemical or '', bold)
                    sheet.write(row, col + 30, record_set.carton or '', bold)

                    sheet.write(row, col + 31, record_set.buyer_arrival or '', bold)
                    sheet.write(row, col + 32, record_set.self_inspection or '', bold)
                    sheet.write(row, col + 33, record_set.buyer_inspection or '', bold)

                    sheet.write(row, col + 34, record_set.readiness_of_cargo or '', bold)
                    sheet.write(row, col + 35, record_set.final_packed or '', bold)
                    sheet.write(row, col + 36, record_set.container_loading or '', date_style)

                    sheet.write(row, col + 37, record_set.health_certificate or '', date_style)
                    sheet.write(row, col + 38, record_set.cfe_certificate or '', date_style)

                    sheet.write(row, col + 39, record_set.buyer_approval_online or '', bold)
                    sheet.write(row, col + 40, record_set.buyer_approval_container or '', bold)
                    sheet.write(row, col + 41, record_set.payment or '', bold)
                    sheet.write(row, col + 42, record_set.container_lifted or '', date_style)
                    sheet.write(row, col + 43, record_set.container_arrival or '', date_style)
                    sheet.write(row, col + 44, record_set.invoice_number or '', bold)
                    sheet.write(row, col + 45, record_set.dispatch_from_factory or '', date_style)

                    sheet.write(row, col + 46, record_set.payment_terms_finance or '', bold)
                    sheet.write(row, col + 47, record_set.adv_payment_date or '', bold)
                    sheet.write(row, col + 48, record_set.funds_received_date or '', bold)
                    sheet.write(row, col + 49, record_set.duty_draw_back_receipt or '', bold)
                    sheet.write(row, col + 50, record_set.rodtep_script_generation or '', bold)

                    sheet.write(row, col + 52, record_set.order_execution_time or '', bold)
                    sheet.write(row, col + 57, record_set.shipment_to_fund_transfer_time or '', bold)

                    sheet.write(row, col + 59, record_set.remarks or '', bold)
                    sheet.write(row, col + 60, record_set.reason or '', bold)
                    sheet.write(row, col + 61, record_set.agent_commission or '', bold)
                    sheet.write(row, col + 62, record_set.po_to_production_timing or '', bold)
                    sheet.write(row, col + 63, record_set.name_of_concern_persons or '', bold)

                    row += 1
                    sec += 1





















