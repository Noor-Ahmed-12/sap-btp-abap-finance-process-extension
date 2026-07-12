CLASS zna_cl_invoice_data DEFINITION PUBLIC FINAL CREATE PUBLIC.
  PUBLIC SECTION.
    METHODS get_sample_invoice RETURNING VALUE(rv_result) TYPE string.
ENDCLASS.

CLASS zna_cl_invoice_data IMPLEMENTATION.
  METHOD get_sample_invoice.
    "-- This source must be imported, adjusted where required, compiled, and activated in an SAP BTP ABAP Environment before it can be described as working SAP code.
    rv_result = 'Draft sample invoice'.
  ENDMETHOD.
ENDCLASS.
