# Architecture

The local Python workflow acts as the working demonstration layer:

CSV / external source
        |
        v
Python integration client
        |
        | Future OData V4
        v
SAP BTP ABAP Environment
        |
        +-- Database table
        +-- CDS views
        +-- RAP business object
        +-- Validations
        +-- Determinations
        +-- Actions
        +-- Service definition
        |
        v
Fiori Elements application
        |
        v
Downstream finance reporting

The repository clearly separates:

- Working local components for validation, lifecycle, persistence, and reporting
- Draft SAP ABAP components that are not yet imported or verified in SAP
- Future SAP trial deployment steps that remain manual
