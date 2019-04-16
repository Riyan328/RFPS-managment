# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
	_inherit = 'res.config.settings'

	gits_system_name = fields.Char(string = "System Name")
	gits_show_documentation = fields.Boolean(string = "Show Documentation")
	gits_show_support = fields.Boolean(string = "Show Support")
	gits_show_account = fields.Boolean(string = "Show Own Account")
	gits_documentation_url = fields.Char(string = "Documentation Url")
	gits_support_url = fields.Char(string = "Support Url")
	gits_account_title = fields.Char(string = "My GITS.com Account Title")
	gits_account_url = fields.Char(string = "My GITS.com Account Url")


	@api.model
	def get_values(self):
		res = super(ResConfigSettings, self).get_values()
		ir_config = self.env['ir.config_parameter'].sudo()
		gits_system_name = ir_config.get_param('gits_system_name', default = 'GITSapp')

		gits_show_documentation = True if ir_config.get_param('gits_show_documentation') == "True" else False
		gits_show_support = True if ir_config.get_param('gits_show_support') == "True" else False
		gits_show_account = True if ir_config.get_param('gits_show_account') == "True" else False

		gits_documentation_url = ir_config.get_param('gits_documentation_url',
													default = 'http://www.greenit.com.np')
		gits_support_url = ir_config.get_param('gits_support_url', default = 'http://www.greenit.com.np/solutions')
		gits_account_title = ir_config.get_param('gits_account_title', default = 'My Online Account')
		gits_account_url = ir_config.get_param('gits_account_url', default = 'http://www.greenit.com.np')
		res.update(
			gits_system_name = gits_system_name,
			gits_show_documentation = gits_show_documentation,
			gits_show_support = gits_show_support,
			gits_show_account = gits_show_account,

			gits_documentation_url = gits_documentation_url,
			gits_support_url = gits_support_url,
			gits_account_title = gits_account_title,
			gits_account_url = gits_account_url
		)
		return res

	@api.multi
	def set_values(self):
		super(ResConfigSettings, self).set_values()
		ir_config = self.env['ir.config_parameter'].sudo()
		ir_config.set_param("gits_system_name", self.gits_system_name or "")
		ir_config.set_param("gits_show_documentation", self.gits_show_documentation or "False")
		ir_config.set_param("gits_show_support", self.gits_show_support or "False")
		ir_config.set_param("gits_show_account", self.gits_show_account or "False")

		ir_config.set_param("gits_documentation_url", self.gits_documentation_url or 
							"http://www.greenit.com.np")
		ir_config.set_param("gits_support_url", self.gits_support_url or "http://www.greenit.com.np/solutions")
		ir_config.set_param("gits_account_title", self.gits_account_title or "My Online Account")
		ir_config.set_param("gits_account_url", self.gits_account_url or "http://www.greenit.com.np")