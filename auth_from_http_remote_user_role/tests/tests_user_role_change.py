# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.tests.common import TransactionCase


class TestUserRoleChange(TransactionCase):

    def setUp(self):
        super().setUp()
        self.groupa = self.env['res.groups'].create({'name': 'group_a'})
        self.groupb = self.env['res.groups'].create({'name': 'group_b'})
        self.groupc = self.env['res.groups'].create({'name': 'group_c'})
        self.rolea = self.env['res.users.role'].create({
            'group_id': self.groupa.id,
            'user_role_code': 'code_A'
        })
        self.roleb = self.env['res.users.role'].create({
            'group_id': self.groupb.id,
            'user_role_code': 'code_B'
        })
        self.rolec = self.env['res.users.role'].create({
            'group_id': self.groupc.id,
            'user_role_code': 'code_C'
        })

    def test_update_user_role(self):
        u = self.env['res.users'].browse(1)
        new_roles = [self.rolea.id, self.roleb.id]
        self.env['res.users.role'].change_roles_remote_user(
            self.env, 1, new_roles)
        self.assertListEqual(u.role_ids.ids, new_roles)

        new_roles = [self.roleb.id, self.rolec.id]
        self.env['res.users.role'].change_roles_remote_user(
            self.env, 1, new_roles)
        self.assertListEqual(u.role_ids.ids, new_roles)

    def test_empty_user_role(self):
        """ last_http_header_roles must be emptied to avoid user failure.

        As removing all roles will also remove all groups, if the user has an
        last_http_header_roles defined it would raise an error 500.

        """
        u = self.env['res.users'].browse(1)
        new_roles = [self.rolea.id, self.roleb.id]
        self.env['res.users.role'].change_roles_remote_user(
            self.env, 1, new_roles)

        u.role_line_ids.unlink()

        self.assertFalse(u.groups_id)
        self.assertFalse(u.last_http_header_roles)
