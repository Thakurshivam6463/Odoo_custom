# Copyright 2013 Agile Business Group sagl (<http://www.agilebg.com>)

from odoo import fields, models, api, _


class TRF(models.Model):
    _inherit = "trf"

    @api.depends("old_revision_ids")
    def _compute_has_old_revisions(self):
        for rec in self:
            rec.has_old_revisions = (
                True if rec.with_context(active_test=False).old_revision_ids else False
            )

    def _compute_has_old_revisions_name(self):
        for rec in self:
            if self.reference:
                rec.unrevisioned_name = self.reference

    current_revision_id = fields.Many2one(
        comodel_name="trf"
    )

    # old_revision_ids = fields.One2many(
    #     comodel_name="trf", 'order_id', string='Order Lines'
    # )

    old_revision_ids = fields.One2many('trf', 'current_revision_id', string='Order Lines')

    revision_number = fields.Integer(string="Revision", copy=False, default=0)
    unrevisioned_name = fields.Char(compute="_compute_has_old_revisions_name",
        string="Original Reference", copy=True, readonly=True
    )
    active = fields.Boolean(default=True)
    has_old_revisions = fields.Boolean(compute="_compute_has_old_revisions")
    revision_count = fields.Integer(
        compute="_compute_revision_count", string="Previous versions count"
    )

    @api.depends("old_revision_ids")
    def _compute_revision_count(self):
        res = self.with_context(active_test=False).read_group(
            domain=[("current_revision_id", "in", self.ids)],
            fields=["current_revision_id"],
            groupby=["current_revision_id"],
        )
        revision_dict = {
            x["current_revision_id"][0]: x["current_revision_id_count"] for x in res
        }
        for rec in self:
            rec.revision_count = revision_dict.get(rec.id, 0)

    @api.returns("self", lambda value: value.id)
    def copy(self, default=None):
        default = default or {}
        if "unrevisioned_name" not in default:
            default["unrevisioned_name"] = False
        rec = super().copy(default=default)
        if not rec.unrevisioned_name:
            name_field = self._context.get("revision_name_field", "name")
            rec.write({"unrevisioned_name": rec[name_field]})
        return rec

    def _get_new_rev_data(self, new_rev_number):
        self.ensure_one()
        return {
            "revision_number": new_rev_number,
            "unrevisioned_name": self.unrevisioned_name,
            "reference": "%s-%02d" % (self.unrevisioned_name, new_rev_number),
            "old_revision_ids": [(4, self.id, False)],
        }

    def _prepare_revision_data(self, new_revision):
        return {"active": False, "current_revision_id": new_revision.id}

    def copy_revision_with_context(self):
        default_data = self.default_get([])
        new_rev_number = self.revision_number + 1
        vals = self._get_new_rev_data(new_rev_number)
        default_data.update(vals)
        new_revision = self.copy(default_data)
        self.old_revision_ids.write({"current_revision_id": new_revision.id})
        self.write(self._prepare_revision_data(new_revision))
        return new_revision

    @api.model
    def create(self, values):
        rec = super().create(values)
        if "unrevisioned_name" not in values:
            name_field = self._context.get("revision_name_field", "name")
            rec.write({"unrevisioned_name": rec[name_field]})
        return rec

    def create_revision(self):
        revision_ids = []
        # Looping over records
        for rec in self:
            # Calling  Copy method
            copied_rec = rec.copy_revision_with_context()
            if hasattr(self, "message_post"):
                msg = _("New revision created: %s") % copied_rec.name
                copied_rec.message_post(body=msg)
                rec.message_post(body=msg)
                rec.rev_no = copied_rec.reference
            revision_ids.append(copied_rec.id)
        action = {
            "type": "ir.actions.act_window",
            "view_mode": "tree,form",
            "name": _("New Revisions"),
            "res_model": self._name,
            "domain": "[('id', 'in', %s)]" % revision_ids,
            "target": "current",
        }
        return action

    #Overwrite as sales.order can be multi-company
    _sql_constraints = [
        (
            "revision_unique",
            "unique(unrevisioned_name, revision_number, company_id)",
            "Order Reference and revision must be unique per Company.",
        )
    ]

    # Extended Code

    def _prepare_revision_data(self, new_revision):
        return {"state": "reject", "active": False, "current_revision_id": new_revision.id}

    def action_view_revisions(self):
        self.ensure_one()
        result = self.env["ir.actions.actions"]._for_xml_id("bz_crm_trf.action_trf")
        result["domain"] = ["|", ("active", "=", False), ("active", "=", True)]
        result["context"] = {
            "active_test": 0,
            "search_default_current_revision_id": self.id,
            "default_current_revision_id": self.id,
        }
        return result
