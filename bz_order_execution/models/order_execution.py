# -*- coding: utf-8 -*-
from odoo import api, fields, models

class OrderExecution(models.Model):
    _name = 'order.execution'
    _rec_name = 'name'

    name = fields.Char(string='Name')
    booked_by = fields.Char(string='Booked By')
    pi_number = fields.Char(string='PI Number')
    order_confirmation_date = fields.Date(string='Date')
    processor = fields.Char(string='Processor')
    po_number = fields.Char(string='PO Number')
    po_date = fields.Date(string='PO Date')
    consignee = fields.Char(string='Consignee')
    order_detail_type = fields.Char(string='Type')
    order_detail_assortment = fields.Char(string='Assortment')
    packing_instructions = fields.Char(string='Packing Instructions')
    loading_instructions = fields.Char(string='Loading Instructions')
    payment_terms = fields.Char(string='Payment Terms')
    shipment_date = fields.Date(string='Shipment Date')

    request_date = fields.Date(string='Request')
    issued_date = fields.Date(string='Issued')
    buyer_approval_date = fields.Char(string='Buyer Approval')
    third_party_lab = fields.Date(string='Third Party Lab')
    test_report = fields.Date(string='Test Reports')
    eia_sample_payment = fields.Date(string='EIA Sample Payment')
    letter_for_drawing_sample = fields.Date(string='Letter for Drawing Sample')
    arrival_eia_collect_sample = fields.Date(string='Arrival of EIA to Collect Sample')
    test_results = fields.Date(string='Test Results')

    draft_from_buyer = fields.Char(string='Draft From Buyer')
    draft_from_printer = fields.Char(string='Draft From Printer')
    buyer_approval = fields.Char(string='Buyer Approval')

    labels_header_cards = fields.Char(string='Labels/Header Cards')
    polythene = fields.Char(string='Polythene')
    chemical = fields.Char(string='Chemical')
    carton = fields.Char(string='Carton')

    buyer_arrival = fields.Char(string='Buyer Arrival')
    self_inspection = fields.Char(string='Self Inspection')
    buyer_inspection = fields.Char(string='Buyer Inspection')

    readiness_of_cargo = fields.Char(string='Readiness of Cargo')
    final_packed = fields.Char(string='Final Packed')
    container_loading = fields.Date(string='Container Loading')

    health_certificate = fields.Date(string='Health Certificate Date')
    cfe_certificate = fields.Date(string='CFE Certificate Date')

    buyer_approval_online = fields.Char(string='Buyer Approval Online')
    buyer_approval_container = fields.Char(string='Buyer Approval Container')
    payment = fields.Char(string='Payment')
    container_lifted = fields.Date(string='Container Lifted')
    container_arrival = fields.Date(string='Container Arrival')
    invoice_number = fields.Char(string='Invoice Number')
    dispatch_from_factory = fields.Date(string='Dispatch From Factory')

    payment_terms_finance = fields.Char(string='Payment Terms')
    adv_payment_date = fields.Char(string='Advance Payment')
    funds_received_date = fields.Char(string='Funds Received')
    duty_draw_back_receipt = fields.Char(string='Duty Draw Back Receipt')
    rodtep_script_generation = fields.Char(string='Rodtep Script Generation')

    order_execution_time = fields.Char(string='Order Execution Time')
    shipment_to_fund_transfer_time = fields.Char(string='Shipment to Fund Transfer Time')
    remarks = fields.Text(string='Remarks')
    reason = fields.Text(string='Reason')
    agent_commission = fields.Char(string='Agent Commission')
    po_to_production_timing = fields.Char(string='PO to Production Timing')
    name_of_concern_persons = fields.Char(string='Name of Concern persons')







