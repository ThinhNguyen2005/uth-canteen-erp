# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_canteen_student = fields.Boolean(
        string="Là sinh viên UTH",
        default=False,
        index=True,
    )
    canteen_student_code = fields.Char(
        string="Mã số sinh viên (MSSV)",
        size=32,
        index=True,
        copy=False,
    )
    canteen_student_class = fields.Char(
        string="Lớp / Khoa",
        size=64,
    )

    _unique_canteen_student_code = models.UniqueIndex(
        "(canteen_student_code) WHERE canteen_student_code IS NOT NULL AND canteen_student_code != ''",
        "Mã số sinh viên (MSSV) phải là duy nhất trên toàn hệ thống!",
    )

    @api.constrains("is_company", "is_canteen_student")
    def _check_student_not_company(self):
        for partner in self:
            if partner.is_company and partner.is_canteen_student:
                raise ValidationError(
                    _("Đối tác loại công ty không thể đánh dấu là sinh viên UTH!")
                )

    @api.constrains("canteen_student_code")
    def _check_canteen_student_code(self):
        partner_model = self.sudo()
        for partner in self:
            code = partner.canteen_student_code
            if not code:
                continue
            if any(ch.isspace() for ch in code):
                raise ValidationError(
                    _("Mã số sinh viên (MSSV) không được chứa khoảng trắng!")
                )
            duplicate_count = partner_model.search_count([
                ("id", "!=", partner.id),
                ("canteen_student_code", "=", code),
            ])
            if duplicate_count:
                raise ValidationError(
                    _("Mã số sinh viên (MSSV) phải là duy nhất trên toàn hệ thống!")
                )
