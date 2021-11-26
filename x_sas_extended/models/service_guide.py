from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ServiceGuide(models.Model):
    _name = 'service.guide'
    _description = 'Service Guide'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    category_id = fields.Many2one('service.category', 'Category', required=True)
    name = fields.Char(string='Number', required=True, readonly=True, default='New', copy=False)
    partner_id = fields.Many2one('res.partner', 'Partner', required=True)
    description = fields.Text()
    guide_price = fields.Float(
        string='Total Cost',
        compute='_compute_price',
        digits='Product Price',
        store=True
    )
    service_guide_line_ids = fields.One2many(comodel_name='service.guide.line', inverse_name='service_guide_id',
                                             string='Guide')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('complete', 'Complete'),
        ('done', 'Finished'),
        ('cancel', 'Cancel')],
        string='State', default='draft', copy=False, tracking=True, group_expand='_expand_groups')
    user_id = fields.Many2one('res.users', 'User', default=lambda self: self.env.user)

    @api.model
    def _expand_groups(self, states, domain, order):
        return ['draft', 'approved', 'complete', 'done', 'cancel']

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('service.guide') or '/'
        return super(ServiceGuide, self).create(vals)

    def action_draft(self):
        self.write({'state': 'draft'})

    def action_approved(self):
        if self.env.user.has_group('x_sas_extended.group_approved'):
            self.write({
                'state': 'approved',
            })
        else:
            raise ValidationError(
                _("You do not have permissions to carry out this process"))

    def action_complete(self):
        self.write({
            'state': 'complete',
        })

    def action_done(self):
        self.write({
            'state': 'done',
        })

    def action_cancel(self):
        self.write({'state': 'cancel'})

    @api.depends('service_guide_line_ids')
    def _compute_price(self):
        for guide in self:
            guide_price = sum(guide.service_guide_line_ids.mapped('price_total'))
            guide.update({
                'guide_price': guide_price
            })

    def table_service_guide(self):
        product = self.service_guide_line_ids
        table_service_guide = ""
        if product:
            table_service_guide += """
            <table width="100%" cellspacing="0" cellpadding="0" style="background-color:#5dc8d8;">
            <thead>
                <tr class="esd-container-frame" width="520" valign="top" align="center">
                    <th style="color: #666666; font-size: 20px; font-family: lora, georgia, times\ new\ roman, serif;"> """ + _('Product') + """ </th>
                    <th style="color: #666666; font-size: 20px; font-family: lora, georgia, times\ new\ roman, serif;"> """ + _('Amount') + """ </th>
                    <th style="color: #666666; font-size: 20px; font-family: lora, georgia, times\ new\ roman, serif;"> """ + _('Discount') + """ </th>
                    <th style="color: #666666; font-size: 20px; font-family: lora, georgia, times\ new\ roman, serif;"> """ + _('Total') + """ </th>
                </tr>
            </thead>
            <tbody>
            """
        for line in product:
            table_service_guide += '<tr class="esd-container-frame" width="520" valign="top" align="center">' + '<td style="color: #666666; font-size: 18px; font-family: lora, georgia, times\ new\ roman, serif;">' + line.product_id.name + "</td>" \
                              + '<td style="color: #666666; font-size: 18px; font-family: lora, georgia, times\ new\ roman, serif;">' + str(line.product_amount) \
                              + '<td style="color: #666666; font-size: 18px; font-family: lora, georgia, times\ new\ roman, serif;">' + str(line.discount) \
                              + '<td style="color: #666666; font-size: 18px; font-family: lora, georgia, times\ new\ roman, serif;">' + str(line.price_total) + "</td>" \
                              + "</td>" + "</tr>"
        if product:
            table_service_guide += "</tbody>" + "</table>"
        return table_service_guide


class ServiceGuideLine(models.Model):
    _name = 'service.guide.line'
    _description = 'Service Guide Line'

    discount = fields.Float(string='Discount')
    product_id = fields.Many2one('product.template', string='Product', domain="[('type', '=', 'service')]")
    product_amount = fields.Float(string='Amount')
    price_total = fields.Float(
        string='Total Cost',
        compute='_compute_price',
        digits='Product Price',
    )
    service_guide_id = fields.Many2one('service.guide', string='Guide Line')
    type = fields.Selection([
        ('consu', 'Consumable'),
        ('service', 'Service')])

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.update({
                'product_amount': self.product_id.list_price,
            })

    @api.depends('product_amount', 'discount')
    def _compute_price(self):
        for guide in self:
            price_total = guide.product_amount * (100-guide.discount)/100
            guide.update({
                'price_total': price_total
            })
