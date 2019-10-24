# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError

STATES = [
    ('uninstallable', 'Uninstallable'),
    ('uninstalled', 'Not Installed'),
    ('installed', 'Installed'),
    ('license', 'Activate Module'),  # is seeking license
    ('to upgrade', 'To be upgraded'),
    ('to remove', 'To be removed'),
    ('to install', 'To be installed'),
]

IES_MODULE_LIST = [
    'ies_base_redeem',
    'ies_coupons',
    'ies_credit_note',
    'ies_giftcards',
    'ies_order_note',
    'ies_pos_brand',
    'ies_pos_commission',
    'ies_pos_product_available',
    'ies_pos_return',
    'ies_voucher'
]


class IESAbstractModel(models.AbstractModel):
    _name = "ies.base"

    ies_name = fields.Char('Name')

    @api.model
    def way_in(self):
        return self.env['ir.module.module'].search([('name', '=', 'ies_base')], limit=1)


class Module(models.Model):
    _inherit = "ir.module.module"

    state = fields.Selection(STATES, string='Status', default='uninstalled', readonly=True, index=True)
    checksum = fields.Char('Checksum')

    @api.multi
    def open_activation_wizard(self):
        return {
            'name': _('Activate'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'ir.module.module.activation',
            'target': 'new',
        }

    @staticmethod
    def get_values_from_terp(terp):
        """Need to find solution for overriding the method"""
        return {
            'description': terp.get('description', ''),
            'shortdesc': terp.get('name', ''),
            'author': terp.get('author', 'Unknown'),
            'maintainer': terp.get('maintainer', False),
            'contributors': ', '.join(terp.get('contributors', [])) or False,
            'website': terp.get('website', ''),
            'license': terp.get('license', 'LGPL-3'),
            'sequence': terp.get('sequence', 100),
            'application': terp.get('application', False),
            'auto_install': terp.get('auto_install', False),
            'icon': terp.get('icon', False),
            'summary': terp.get('summary', ''),
            'url': terp.get('url') or terp.get('live_test_url', ''),
        }

    @api.multi
    def _button_immediate_function(self, function):
        pass_flag = False
        for rec in self:
            if rec.name in IES_MODULE_LIST and not self.env.context.get('active'):
                rec.state = 'license'
                pass_flag = True
        if pass_flag:
            return True
        return super(Module, self)._button_immediate_function(function)

    @api.multi
    def module_uninstall(self):
        for rec in self:
            if rec.name == 'ies_base':
                raise UserError(_("The `ies_base` module cannot be uninstalled"))
            res = super(Module, self).module_uninstall()
            rec.write({'checksum': False})
            return res
