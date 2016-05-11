from openerp import models, fields, api
from datetime import date
import StringIO
import base64

class Product(models.Model):
    _inherit = 'product.template'

    qty_low_stock_notify = fields.Integer(string='Notify for Qty Below', default=80,
                                          help='When stock on hand falls below this number, it will be included in the low stock report. Set to -1 to exclude from the report.')

    def send_low_stock_via_email(self, cr, uid, context=None):
        header_label_list=["SKU", "Name", "Qty On Hand","Qty Incoming","Low Stock Qty"]
        ## Get email template
        template_obj = self.pool.get('mail.template')
        template_ids = template_obj.search(cr, uid, [('name', '=', 'Low Stock Automated Report')])
        template     = template_obj.browse(cr, uid, template_ids)
        if template:
            default_body = template.body_html
            custom_body  = """
                <table>
                    <th>%s</th>
                    <th>%s</th>
                    <th style="text-align:center;">%s</th>
                    <th style="text-align:center;">%s</th>
                    <th style="text-align:center;">%s</th>
            """ %(header_label_list[0], header_label_list[1], header_label_list[2], header_label_list[3], header_label_list[4])
            ## Check for low stock products
            product_obj  = self.pool.get('product.product')
            product_ids  = product_obj.search(cr, uid, [('active', '=', True), ('sale_ok', '=', True), ('default_code', '!=', False)])
            for product in product_obj.browse(cr, uid, product_ids):
                product_sku = product.default_code
                if not product_sku or product_sku == '':
                    continue
                qty_available = product.qty_available
                qty_incoming  = product.incoming_qty
                qty_low_stock_notify = product.qty_low_stock_notify
                if qty_available <= qty_low_stock_notify and qty_low_stock_notify >= 0: ## set low_stock_notify = -1 to never be notified
                    custom_body += """
                        <tr style="font-size:14px;">
                            <td>%s</td>
                            <td>%s</td>
                            <td style="text-align:center;">%s</td>
                            <td style="text-align:center;">%s</td>
                            <td style="text-align:center;">%s</td>
                        </tr>
                    """ %(product_sku, product.name, str(qty_available), str(qty_incoming), str(qty_low_stock_notify))
            custom_body  += "</table>"
            template.body_html = default_body + custom_body
            send_email         = template_obj.send_mail(cr, uid, template.id, uid, force_send=True, context=context)
            template.body_html = default_body
            return True
