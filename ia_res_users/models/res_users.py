# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, tools, models, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


_logger = logging.getLogger(__name__)

class Users(models.Model):
    _inherit = "res.users"
    @api.model
    @tools.ormcache('self._uid')
    def context_get(self):
        user = self.env.user
        # determine field names to read
        name_to_key = {
            name: name[8:] if name.startswith('context_') else name
            for name in self._fields
            if name.startswith('context_') or name in ('lang', 'tz')
        }
        # use read() to not read other fields: this must work while modifying
        # the schema of models res.users or res.partner
        values = user.read(list(name_to_key), load=False)[0]
        return {
            key: values[name]
            for name, key in name_to_key.items()
        }