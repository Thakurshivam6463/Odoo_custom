odoo.define('bz_purchase_dashboard.Dashboard', function (require) {
"use strict";

var AbstractAction = require('web.AbstractAction');
var core = require('web.core');
var QWeb = core.qweb;
var rpc = require('web.rpc');
var ajax = require('web.ajax');
var _t = core._t;

var PoDashboard = AbstractAction.extend({
    template: 'Dashboard',

    events: {
             'click .po_rfq':'po_rfq',
             'click .purchase_order':'purchase_order',
             'click .purchase_done':'purchase_done',
             'click .purchase_cancel':'purchase_cancel',
             'click .po_requisition_draft':'po_requisition_draft',
             'click .po_requisition_confirmed':'po_requisition_confirmed',
             'click .po_requisition_ongoing':'po_requisition_ongoing',
             'click .po_management':'po_management',
             'click .po_administration':'po_administration',
             'click .po_sales':'po_sales'

    },

     init: function(parent, context) {
     this._super(parent, context);
     this.dashboards_templates = ['RfqDetails'];
     this.today_rfq = [];
     },

     start: function () {
        var self = this;
        this.set("title", 'Dashboard');
        return this._super().then(function() {
                self.render_dashboards();
            });
    },

     render_dashboards: function() {
     console.log("Render Dashboard")
        var self = this;
        _.each(this.dashboards_templates, function(template) {
            self.$('.o_purchase_dashboard').append(QWeb.render(template, {widget: self}));
        });
     },

     willStart: function(){
        var self = this;
        return $.when([ajax.loadLibs(this), this._super()]).then(function() {
            return self.fetch_data();
        });
    },

     fetch_data: function() {
        var self = this;
        var def0 =  self._rpc({
                model: 'purchase.order',
                method: 'check_rfq'
        }).then(function(result) {
            self.total_rfq = result['total_rfq']
            console.log(self.total_rfq)
        });
        var def1 =  self._rpc({
                model: 'purchase.order',
                method: 'check_purchase_order'
        }).then(function(result) {
            self.total_po = result['total_po']
        });
        var def2 =  self._rpc({
                model: 'purchase.order',
                method: 'check_purchase_done'
        }).then(function(result) {
            self.total_po_done = result['total_po_done']
        });
        var def3 =  self._rpc({
                model: 'purchase.order',
                method: 'check_purchase_cancel'
        }).then(function(result) {
            self.total_po_cancel = result['total_po_cancel']
        });
        var def4 =  self._rpc({
                model: 'purchase.order',
                method: 'check_management_po'
        }).then(function(result) {
            self.total_management_po = result['total_management_po']
            self.management_po = result['management_po']
        });
        var def5 =  self._rpc({
                model: 'purchase.order',
                method: 'check_administration_po'
        }).then(function(result) {
            self.total_administration_po = result['total_administration_po']
            self.administration_po = result['administration_po']
        });
        var def6 =  self._rpc({
                model: 'purchase.order',
                method: 'check_sales_po'
        }).then(function(result) {
            self.total_sales_po = result['total_sales_po']
            self.sales_po = result['sales_po']
        });
        var def7 =  self._rpc({
                model: 'purchase.requisition',
                method: 'check_purchase_requisition_draft'
        }).then(function(result) {
            self.total_po_requisition_draft = result['total_po_requisition_draft']
        });
        var def8 =  self._rpc({
                model: 'purchase.requisition',
                method: 'check_purchase_requisition_confirmed'
        }).then(function(result) {
            self.total_po_requisition_confirmed = result['total_po_requisition_confirmed']
        });
        var def8 =  self._rpc({
                model: 'purchase.requisition',
                method: 'check_purchase_requisition_ongoing'
        }).then(function(result) {
            self.total_po_requisition_ongoing = result['total_po_requisition_ongoing']
        });
        return $.when(def0, def1, def2, def3, def4, def5, def6, def7, def8);
    },

    //events

        po_rfq: function(ev){
            var self = this;
            ev.stopPropagation();
            ev.preventDefault();
            console.log('entered function RFQ')

            var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };

            this.do_action({
                name: _t("Requests for Quotation"),
                type: 'ir.actions.act_window',
                res_model: 'purchase.order',
                view_mode: 'tree,form,calendar',
                views: [[false, 'list'],[false, 'form']],
                domain: [['state','in',['draft']]],
                target: 'current' //self on some of them
            }, {
                    on_reverse_breadcrumb: this.on_reverse_breadcrumb
            });
        },

        purchase_order: function(ev){
            var self = this;
            ev.stopPropagation();
            ev.preventDefault();

            var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };

            this.do_action({
                name: _t("Requests for Quotation"),
                type: 'ir.actions.act_window',
                res_model: 'purchase.order',
                view_mode: 'tree,form,calendar',
                views: [[false, 'list'],[false, 'form']],
                domain: [['state','in',['purchase']]],
                target: 'current' //self on some of them
            }, {
                    on_reverse_breadcrumb: this.on_reverse_breadcrumb
            });
        },

        purchase_done: function(ev){
            var self = this;
            ev.stopPropagation();
            ev.preventDefault();

            var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };

            this.do_action({
                name: _t("Requests for Quotation"),
                type: 'ir.actions.act_window',
                res_model: 'purchase.order',
                view_mode: 'tree,form,calendar',
                views: [[false, 'list'],[false, 'form']],
                domain: [['state','in',['done']]],
                target: 'current' //self on some of them
            }, {
                    on_reverse_breadcrumb: this.on_reverse_breadcrumb
            });
        },

        purchase_cancel: function(ev){
            var self = this;
            ev.stopPropagation();
            ev.preventDefault();
            var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };

            this.do_action({
                name: _t("Requests for Quotation"),
                type: 'ir.actions.act_window',
                res_model: 'purchase.order',
                view_mode: 'tree,form,calendar',
                views: [[false, 'list'],[false, 'form']],
                domain: [['state','in',['cancel']]],
                target: 'current' //self on some of them
            }, {
                    on_reverse_breadcrumb: this.on_reverse_breadcrumb
            });
        },

        po_requisition_draft: function(ev){
            var self = this;
            ev.stopPropagation();
            ev.preventDefault();
            var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };

            this.do_action({
                name: _t("Purchase Agreements"),
                type: 'ir.actions.act_window',
                res_model: 'purchase.requisition',
                view_mode: 'tree,form,calendar',
                views: [[false, 'list'],[false, 'form']],
                    domain: [['state','in',['draft']]],
                target: 'current' //self on some of them
            }, {
                    on_reverse_breadcrumb: this.on_reverse_breadcrumb
            });
        },
        po_requisition_confirmed: function(ev){
            var self = this;
            ev.stopPropagation();
            ev.preventDefault();
            var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };

            this.do_action({
                name: _t("Purchase Agreements"),
                type: 'ir.actions.act_window',
                res_model: 'purchase.requisition',
                view_mode: 'tree,form,calendar',
                views: [[false, 'list'],[false, 'form']],
                    domain: [['state','in',['in_progress']]],
                target: 'current' //self on some of them
            }, {
                    on_reverse_breadcrumb: this.on_reverse_breadcrumb
            });
        },
        po_requisition_ongoing: function(ev){
            var self = this;
            ev.stopPropagation();
            ev.preventDefault();
            var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };

            this.do_action({
                name: _t("Purchase Agreements"),
                type: 'ir.actions.act_window',
                res_model: 'purchase.requisition',
                view_mode: 'tree,form,calendar',
                views: [[false, 'list'],[false, 'form']],
                    domain: [['state','in',['ongoing']]],
                target: 'current' //self on some of them
            }, {
                    on_reverse_breadcrumb: this.on_reverse_breadcrumb
            });
        },

        po_management: function(ev){
            var self = this;
            ev.stopPropagation();
            ev.preventDefault();
            var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };

            this.do_action({
                name: _t("Requests for Quotation"),
                type: 'ir.actions.act_window',
                res_model: 'purchase.order',
                view_mode: 'tree,form,calendar',
                views: [[false, 'list'],[false, 'form']],
                    domain: [['id','=', self.management_po]],
                target: 'current' //self on some of them
            }, {
                    on_reverse_breadcrumb: this.on_reverse_breadcrumb
            });
        },

        po_administration: function(ev){
            var self = this;
            ev.stopPropagation();
            ev.preventDefault();
            var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };

            this.do_action({
                name: _t("Requests for Quotation"),
                type: 'ir.actions.act_window',
                res_model: 'purchase.order',
                view_mode: 'tree,form,calendar',
                views: [[false, 'list'],[false, 'form']],
                    domain: [['id','=', self.administration_po]],
                target: 'current' //self on some of them
            }, {
                    on_reverse_breadcrumb: this.on_reverse_breadcrumb
            });
        },

        po_sales: function(ev){
            var self = this;
            ev.stopPropagation();
            ev.preventDefault();
            var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };

            this.do_action({
                name: _t("Requests for Quotation"),
                type: 'ir.actions.act_window',
                res_model: 'purchase.order',
                view_mode: 'tree,form,calendar',
                views: [[false, 'list'],[false, 'form']],
                    domain: [['id','=', self.sales_po]],
                target: 'current' //self on some of them
            }, {
                    on_reverse_breadcrumb: this.on_reverse_breadcrumb
            });
        },


    });

core.action_registry.add('purchase_dashboard_tag', PoDashboard);

return PoDashboard;

});