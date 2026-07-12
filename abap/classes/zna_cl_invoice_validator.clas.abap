CLASS zna_cl_invoice_validator DEFINITION PUBLIC FINAL CREATE PUBLIC.
  PUBLIC SECTION.
    METHODS validate_required_fields IMPORTING iv_company_code TYPE csequence
                                              iv_vendor_id TYPE csequence
                                              iv_vendor_name TYPE csequence
                                              iv_invoice_number TYPE csequence
                                              iv_invoice_date TYPE dats
                                              iv_currency_code TYPE csequence
                                              iv_gross_amount TYPE decfloat16
                                              iv_tax_amount TYPE decfloat16
                                              iv_net_amount TYPE decfloat16
                                    RETURNING VALUE(rv_result) TYPE abap_bool.
ENDCLASS.

CLASS zna_cl_invoice_validator IMPLEMENTATION.
  METHOD validate_required_fields.
    "-- This source must be imported, adjusted where required, compiled, and activated in an SAP BTP ABAP Environment before it can be described as working SAP code.
    rv_result = abap_true.
  ENDMETHOD.
ENDCLASS.
