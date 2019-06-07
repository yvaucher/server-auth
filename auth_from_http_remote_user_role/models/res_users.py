# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    last_http_header_roles = fields.Char(
        string='Last HTTP header roles'
    )

    def reset_last_http_header_roles(self):
        """ Reset last_http_header_roles

        With last_http_header_roles filled and without roles a user end up
        without access and would get a 500 error.

        """
        for user in self:
            if not user.role_line_ids:
                user.last_http_header_roles = False
