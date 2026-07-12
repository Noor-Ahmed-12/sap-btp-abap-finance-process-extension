# Data model

The invoice entity contains the following fields:

- invoice_uuid
- company_code
- vendor_id
- vendor_name
- invoice_number
- invoice_date
- currency_code
- gross_amount
- tax_amount
- net_amount
- cost_center
- description
- processing_status
- rejection_reason
- error_message
- created_by
- created_at
- last_changed_by
- last_changed_at

The local Python model uses UUID strings, ISO dates, UTC timestamps, and Decimal for financial values.
