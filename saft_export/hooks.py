# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "saft_export"
app_title = "Saft Export"
app_publisher = "SMB"
app_description = "SAF-T XML Export"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "jay@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/saft_export/css/saft_export.css"
# app_include_js = "/assets/saft_export/js/saft_export.js"

# include js, css files in header of web template
# web_include_css = "/assets/saft_export/css/saft_export.css"
# web_include_js = "/assets/saft_export/js/saft_export.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "saft_export.utils.get_home_page"

website_route_rules = [
	{ "from_route": "/project1/<path:so_name>", "to_route": "project1" },
 ]

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "saft_export.install.before_install"
# after_install = "saft_export.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "saft_export.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"saft_export.tasks.all"
# 	],
# 	"daily": [
# 		"saft_export.tasks.daily"
# 	],
# 	"hourly": [
# 		"saft_export.tasks.hourly"
# 	],
# 	"weekly": [
# 		"saft_export.tasks.weekly"
# 	]
# 	"monthly": [
# 		"saft_export.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "saft_export.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "saft_export.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "saft_export.task.get_dashboard_data"
# }
