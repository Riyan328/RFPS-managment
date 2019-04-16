# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import datetime
import base64
from werkzeug.urls import url_encode



class NewTender(models.Model):
	_name = "new.tender"
	_description = "All About Managment of Tender Notice"
	_inherit = ['mail.thread', 'mail.activity.mixin']




	name = fields.Char(string="Name of Company", required = True, search = "_search_name",
		track_visibility = True, states = {'cancel': [('readonly', True)], 'done': [('readonly', True)]})
	street = fields.Char(string = "Street", required = True, 
		states = {'cancel': [('readonly', True)], 'done': [('readonly', True)]})
	street2 = fields.Char(string = "Street2", required = True, 
		states = {'cancel': [('readonly', True)], 'done': [('readonly', True)]})
	city = fields.Char(string = "City", required = True, 
		states = {'cancel': [('readonly', True)], 'done': [('readonly', True)]})
	category = fields.Many2one('catelog.category', string = "Category", required = True, 
		states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
	publ_date = fields.Datetime(string = "Tender Published Date", required = True,
		states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
	# selection between days and date in tender dates
	field_type = fields.Selection([('days','Days'), ('date','Date')], 'Bond Submisson', default = "date",
		states = {'cancel': [('readonly', True)], 'done': [('readonly', True)]})
	subm_days = fields.Integer(string = "Expiry Days", states = {'cancel': [('readonly', True)], 'done': [('readonly', True)]})
	subm_date = fields.Datetime(string = "Tender Submisson Date", required = True, states = {'cancel': [('readonly', True)], 'done': [('readonly', True)]})
	days_left = fields.Char(string = "Remaining Days", compute = '_check_days', states = {'cancel': [('readonly', True)], 'done': [('readonly', True)]})
	tender_expire = fields.Integer(default = 0)
	# condition for percent or amount
	bond_amount = fields.Selection([('percentage','Percentage'), ('amount','Amount')], string = "Bid Bond Amount" , default = "amount", store = True,
		states = {'cancel': [('readonly', True)], 'done': [('readonly', True)]})
	percentage = fields.Float(string = "Percentage of Bid Amount", states = {'cancel': [('readonly', True)], 'done': [('readonly', True)]},
		help = 'The percentage value should be in Decimal')
	amount = fields.Float(string = "Bond Amount", states = {'cancel': [('readonly', True)], 'done': [('readonly', True)]})
	bid_amount = fields.Float(string = "Bond Amount/Percentage", compute = '_check_value')
	# condition for percent or amount
	image = fields.Binary(string = "Tender Notice Image", states = {'cancel': [('readonly', True)], 'done': [('readonly', True)]})
	state = fields.Selection([('record','Record'), 
							  ('draft','Draft'),
							  ('sent','Sent'),
							  ('done', 'Locked'),
							  ('tendered','Tendered'),
							  ('cancel', 'Cancelled'),
							  ], string = "Status", copy = False, track_visibility = 'onchange', default = 'record')
	# calling the notebook page
	myprod_id = fields.One2many('tender.product', 'product_parent', string = "Order Products", states = {'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy = True, auto_join = True)
	note = fields.Text(string = "Notes", states = {'cancel': [('readonly', True)], 'done': [('readonly', True)]})
	upload_file = fields.Binary(string="Upload File", states = {'cancel': [('readonly', True)], 'done': [('readonly', True)]})
	file_name = fields.Char(string="File Name", states = {'cancel': [('readonly', True)], 'done': [('readonly', True)]})
	bank_id = fields.Boolean(string = "Bank Gaurantee", 
		states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
	contract_id = fields.Char(string = "Contract No. and Date", 
		states={'cancel': [('readonly', True)], 'done': [('readonly', True)]})
	
	

	@api.multi
	def unlink(self):
		for tender in self:
			if tender.state not in ('record', 'cancel'):
				raise UserError("You can not delete a confirmed quotation or a record whose docs are requested. You must first cancel it.")
			return super(NewTender, self).unlink()
	pass


	@api.one
	@api.constrains('publ_date','subm_date')
	def _check_date(self):
		if self.subm_date < self.publ_date:
			raise ValidationError("The submisson date should be geater then published date!!!")
			pass


	@api.model	
	@api.onchange('publ_date', 'subm_days')
	def _calculate_date(self):
		if self.publ_date and self.subm_days:
		    planned = self.publ_date + datetime.timedelta(days = self.subm_days)
		    self.subm_date = planned


	@api.one
	@api.depends('subm_date')
	def _check_days(self):
		if self.subm_date:
		    current_date = datetime.datetime.now()
		    rdy = self.subm_date - current_date
		    self.days_left = rdy.days + 1
		if int(self.days_left) < int(self.tender_expire):
			expire = ('Tender is Expired')
			self.days_left = expire
		pass
	

	@api.one
	@api.constrains('percentage')
	def _check_percentage(self):
		if self.percentage >100 or self.percentage <0:
			raise ValidationError("The percentage cannot be negative or greater than 100!!!")


	@api.model
	@api.onchange('percentage', 'amount')
	def _check_value(self):
		for each in self:
			each.bid_amount = each.percentage * 100 or each.amount
	pass


	#To send mail on creation of a new record
	@api.model
	def create(self, values):
		rec = super(NewTender, self).create(values)
		#here "rec" is an id that gets value from the action_mail_send
		template = self.env.ref('riyan_module.notification_email_template_id')
		template.send_mail(rec.id, force_send = True)
		#rec.action_mail_send()
		return rec


	#To access all the group users to send mail
	@api.multi
	def task_send_mail(self):
		user_group = self.env.ref("riyan_module.group_user")
		email_list = [user.partner_id.email for user in user_group.users if user.partner_id.email]
		return ",".join(email_list)
		

	#To send the link to access the tender Record
	@api.multi
	def action_mail_send(self):
		base_url = self.env['ir.config_parameter'].get_param('web.base.url')
		url_params= {
			'id': self.id,
			'action': self.env.ref('riyan_module.action_record_form').id,
		 	'model': 'new.tender',
		 	'view_type': 'form',
		 	'menu_id': self.env.ref('riyan_module.tender_menu_record').id,
		}
		params = '/web?#%s' % url_encode(url_params)
		param = base_url + params
		return param

		

	#send email with a pop-up to edit the template
	@api.multi
	def send_mail_template(self):
		self.ensure_one()
		ir_model_data = self.env['ir.model.data']
		try:
		    template_id = ir_model_data.get_object_reference('riyan_module', 'tenderemail_templet')[1]
		except ValueError:
			template_id = False
		try:
		    compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
		except ValueError:
			compose_form_id = False
		ctx = {
		    'default_model': 'new.tender',
		    'default_res_id': self.ids[0],
		    'default_use_template': bool(template_id),
		    'default_template_id': template_id,
		    'default_composition_mode': 'comment',
		    'mark_so_as_sent': True,
		    'force_email': True
		}
		return {
		    'type': 'ir.actions.act_window',
		    'view_type': 'form',
		    'view_mode': 'form',
		    'res_model': 'mail.compose.message',
		    'views': [(compose_form_id,'form')],
		    'view_id': compose_form_id,
		    'target': 'new',
		    'context': ctx,
		}
		pass
		

	@api.multi
	def action_cancel(self):
		return self.write({'state': 'cancel'})
		pass


	@api.multi
	def action_record(self):
		return self.write({'state': 'record'})
		pass


	@api.multi
	def action_done(self):
		return self.write({'state': 'done'})
		pass


	@api.multi
	def action_unlock(self):
		self.write({'state': 'tendered'})
		pass


	@api.multi
	def action_confirm(self):
		return self.write({'state': 'draft'})
		pass


	@api.multi
	def action_email_send(self):
		return self.write({'state': 'sent'})
		pass





#The notebook page model
class myproduct(models.Model):
	_name = "tender.product"
	_description = "Product order line"


	product_parent = fields.Many2one('new.tender', string = "Order")
	prod_id = fields.Many2one('vendor.product', string = "Product Name")
	specification = fields.Char(string = "Description", store = True, related = "prod_id.specification")
	qty = fields.Float(string = "Required Qty")
	rate =fields.Float(string = "Unit Price", store = True, related = "prod_id.pro_price")
	maf = fields.Boolean(string = "MAF")
	total = fields.Float(string = "Total Price", compute = "_unit_total")
	

	@api.depends('qty', 'rate')
	def _unit_total(self):
		for record in self:
			if record.qty and record.rate:
				pt = record.qty * record.rate
				record.total = pt

