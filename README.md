# Low Stock Notification

_low_stock_notify_ is a module that automatically emails a list of products with low stock. 

Each product's low stock "threshold" is set on the product form. 
- Default value is 80
- Set to (-1) for the product to be excluded from the low stock report
- Only products who are "sellable" will be included

Creates a scheduled action to run once daily. 
- You can reconfigure the settings in ```Settings > Automation > Scheduled Actions > Check Low Stock and Notify```

Includes a very basic email template, but **you must update email address values on the template settings**.
- You can change the settings in ```Settings > Email > Templates > Low Stock Automated Report```

##### To Do:

- Test in default instance
  - Does SKU work appropriately?
- Test what happens if there are multiple templates named _Low Stock Automated Report_
