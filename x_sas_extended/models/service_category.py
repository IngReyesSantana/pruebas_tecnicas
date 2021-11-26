from odoo import fields, models, api


class ServiceCategory(models.Model):
    _name = 'service.category'
    _description = 'Service Category'

    active = fields.Boolean(string='Active')
    name = fields.Char(string='Category')
