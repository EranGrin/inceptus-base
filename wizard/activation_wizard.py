# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
# import httplib
import urllib
import json
import http


class ConfigWiz(models.TransientModel):
    _name = 'ies.product.config.settings'
    _inherit = 'res.config.settings'
    _description = "IES Product Configuration"


class Activation(models.TransientModel):
    _name = "ir.module.module.activation"
    _description = "IR Module Activation"

    license = fields.Char('License', required=1)

    # @api.multi
    def activate_product(self):
        module_id = self.env.context.get('active_id')
        module_rec = self.env['ir.module.module'].browse(module_id)
        module_rec.with_context(active=1).button_immediate_install()
        module_rec.write({'checksum': '1', 'state': 'installed'})
        # params = urllib.parse.urlencode({
        #     'edd_action': 'activate_license',
        #     'license': self.license,
        #     'item_name': module_rec.shortdesc,
        #     'url': self.env['ir.config_parameter'].get_param('web.base.url')
        # })
        # headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        # url = self.env['ir.config_parameter'].get_param('inceptus.module.activate.url')
        # conn = http.client.HTTPConnection(url)
        # conn.request("POST", "/edd-sl", params, headers)
        # response = conn.getresponse()
        # sl_data = response.read()
        # activation_data = json.loads(sl_data)
        # if activation_data.get('success'):
        #     module_rec.with_context(active=1).button_immediate_install()
        #     module_rec.write({'checksum': activation_data.get('checksum'), 'state': 'installed'})
        # else:
        #     raise ValidationError(
        #         _('Error!\nInceptus License Server cannot verify the entered license for this product.\n%s' % (
        #             activation_data.get('error'))))
        # conn.close()
