You are building a portfolio project for a junior SAP software engineering application.

## Project identity

Repository name:

```text
sap-btp-abap-finance-process-extension
```

Project title:

```text
SAP BTP ABAP Finance Process Extension
```

Project status:

```text
In Progress
```

Project start date:

```text
July 2026
```

GitHub owner:

```text
Noor-Ahmed-12
```

Expected future repository URL:

```text
https://github.com/Noor-Ahmed-12/sap-btp-abap-finance-process-extension
```

## Main objective

Build an educational finance invoice-processing application that demonstrates:

* SAP BTP ABAP Environment concepts
* ABAP Cloud
* ABAP Objects
* Open SQL
* Core Data Services
* RESTful Application Programming Model
* OData V4
* Fiori Elements concepts
* Clean Core principles
* Released API concepts
* Python-to-SAP integration
* End-to-end data tracing
* Finance workflow validation
* Testing and documentation

The project must be honest about its status.

Do not claim:

* Production deployment
* Commercial SAP S/4HANA access
* Real invoice posting
* Real vendor or company data
* Successful SAP deployment unless it has actually been completed
* Screenshots that do not exist
* APIs that were not tested

The local Python portion must work independently before the SAP environment is connected.

## Business problem

Finance teams may receive invoice records from CSV files, internal systems, APIs, and manual forms.

These records may contain:

* Missing required fields
* Duplicate invoices
* Invalid amounts
* Incorrect tax calculations
* Unsupported currencies
* Invalid workflow status changes
* Missing rejection reasons
* Inconsistent data across systems

The application should validate invoice records and move them through a controlled workflow.

## Invoice lifecycle

Use these statuses:

```text
NEW
VALIDATED
APPROVED
REJECTED
POSTED
```

Allowed transitions:

```text
NEW -> VALIDATED
NEW -> REJECTED
VALIDATED -> APPROVED
VALIDATED -> REJECTED
REJECTED -> NEW
APPROVED -> POSTED
```

Blocked transitions include:

```text
NEW -> POSTED
REJECTED -> POSTED
POSTED -> APPROVED
POSTED -> NEW
```

Posted invoices must be treated as read-only.

## Business rules

Implement these rules in the local Python application:

1. Invoice UUID must be unique.
2. Company code is required.
3. Vendor ID is required.
4. Vendor name is required.
5. Invoice number is required.
6. Invoice date is required.
7. Currency must be one of:

```text
EUR
USD
GBP
CHF
```

8. Gross amount must be greater than zero.
9. Tax amount cannot be negative.
10. Net amount cannot be negative.
11. Net amount plus tax amount must equal gross amount within a tolerance of 0.01.
12. Vendor ID plus invoice number must be unique.
13. Only a `NEW` invoice can be validated.
14. Only a `VALIDATED` invoice can be approved.
15. A `NEW` or `VALIDATED` invoice can be rejected.
16. A rejected invoice requires a rejection reason.
17. Only an `APPROVED` invoice can be posted.
18. A posted invoice cannot be modified.
19. All validation failures must return understandable messages.
20. Do not expose passwords, tokens, private service URLs, or credentials.

## Data model

Use these fields:

```text
invoice_uuid
company_code
vendor_id
vendor_name
invoice_number
invoice_date
currency_code
gross_amount
tax_amount
net_amount
cost_center
description
processing_status
rejection_reason
error_message
created_by
created_at
last_changed_by
last_changed_at
```

Use:

* UUID strings for `invoice_uuid`
* ISO date format for `invoice_date`
* ISO 8601 UTC timestamps
* Decimal instead of float for financial calculations
* Uppercase workflow statuses
* Uppercase currency codes

## Repository structure

Create this structure:

```text
sap-btp-abap-finance-process-extension/
│
├── README.md
├── LICENSE
├── .gitignore
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
│
├── docs/
│   ├── architecture.md
│   ├── business-requirements.md
│   ├── business-rules.md
│   ├── data-model.md
│   ├── api-contract.md
│   ├── sap-setup.md
│   ├── testing.md
│   ├── clean-core.md
│   └── screenshots/
│       └── README.md
│
├── diagrams/
│   ├── system-architecture.mmd
│   ├── invoice-lifecycle.mmd
│   └── data-model.mmd
│
├── sample-data/
│   ├── valid_invoices.csv
│   ├── invalid_invoices.csv
│   └── duplicate_invoices.csv
│
├── python-client/
│   ├── README.md
│   ├── .env.example
│   ├── src/
│   │   └── sap_finance_extension/
│   │       ├── __init__.py
│   │       ├── config.py
│   │       ├── models.py
│   │       ├── exceptions.py
│   │       ├── validators.py
│   │       ├── lifecycle.py
│   │       ├── csv_loader.py
│   │       ├── local_repository.py
│   │       ├── sap_odata_client.py
│   │       ├── reporting.py
│   │       └── cli.py
│   └── tests/
│       ├── __init__.py
│       ├── test_validators.py
│       ├── test_lifecycle.py
│       ├── test_csv_loader.py
│       ├── test_repository.py
│       └── test_reporting.py
│
└── abap/
    ├── README.md
    ├── database-tables/
    │   └── zna_invoice.ddls.asddl
    ├── cds-views/
    │   ├── zna_i_invoice.ddls.asddl
    │   └── zna_c_invoice.ddls.asddl
    ├── behavior/
    │   ├── zna_i_invoice.bdef.asbdef
    │   └── zbp_na_i_invoice.clas.abap
    ├── services/
    │   ├── zna_sd_invoice.srvd.srvdsrv
    │   └── zna_ui_invoice_o4.README.md
    ├── classes/
    │   ├── zna_cl_invoice_validator.clas.abap
    │   └── zna_cl_invoice_data.clas.abap
    └── tests/
        └── zna_cl_invoice_validator_test.clas.abap
```

## Scope for this Codex run

Complete the local project foundation now.

The following must work locally:

* CSV loading
* Invoice validation
* Duplicate detection
* Workflow transitions
* Local persistence
* Finance summary reporting
* Command-line interface
* Automated tests
* Documentation
* Mermaid diagrams

Create SAP ABAP source drafts, but clearly label them as:

```text
Draft source for import and verification in SAP BTP ABAP Environment
```

Do not state that those files have compiled unless they have actually been imported and activated in SAP.

## Python requirements

Use:

```text
Python 3.11+
```

Prefer the standard library where practical.

Allowed runtime dependencies:

```text
requests
python-dotenv
```

Allowed development dependencies:

```text
pytest
pytest-cov
ruff
mypy
```

Avoid unnecessary frameworks.

Use type hints throughout.

Use docstrings for public classes and functions.

Use `Decimal` for financial values.

Use custom exception classes.

Do not silently ignore invalid records.

## Python model

Create an `Invoice` dataclass.

Suggested fields:

```python
invoice_uuid: str
company_code: str
vendor_id: str
vendor_name: str
invoice_number: str
invoice_date: date
currency_code: str
gross_amount: Decimal
tax_amount: Decimal
net_amount: Decimal
cost_center: str
description: str
processing_status: InvoiceStatus
rejection_reason: str | None
error_message: str | None
created_by: str
created_at: datetime
last_changed_by: str
last_changed_at: datetime
```

Create an `InvoiceStatus` string enum.

## Validation design

Create reusable validation functions.

Required functions should include equivalents of:

```python
validate_required_fields(invoice)
validate_currency(invoice)
validate_amounts(invoice)
validate_amount_reconciliation(invoice)
validate_duplicate_invoice(invoice, existing_invoices)
validate_invoice(invoice, existing_invoices)
```

Return structured validation errors or raise a documented custom exception.

A validation error should include:

```text
field
code
message
```

Example:

```text
gross_amount
INVALID_AMOUNT
Gross amount must be greater than zero.
```

## Workflow service

Create a lifecycle service with methods equivalent to:

```python
validate(invoice)
approve(invoice)
reject(invoice, reason)
reopen(invoice)
post(invoice)
```

Each method must:

* Check the current status
* Reject invalid transitions
* Update the status
* Update modification metadata
* Return the updated invoice

Create a custom exception:

```python
InvalidStatusTransitionError
```

## Local repository

Create a local JSON-backed repository for the working demonstration.

It should support:

```python
add(invoice)
get(invoice_uuid)
list_all()
update(invoice)
delete(invoice_uuid)
find_by_vendor_and_invoice_number(vendor_id, invoice_number)
```

Store runtime data in:

```text
local-data/invoices.json
```

Add `local-data/` to `.gitignore`.

The repository should create the file automatically when needed.

## CSV loader

Load CSV rows into invoice objects.

The loader must:

* Validate headers
* Parse ISO dates
* Parse Decimal values
* Normalize currency and status
* Report row-level errors
* Avoid crashing the entire import because of one invalid row
* Return successful records and failed records separately

## Sample CSV files

Use this header:

```csv
invoice_uuid,company_code,vendor_id,vendor_name,invoice_number,invoice_date,currency_code,gross_amount,tax_amount,net_amount,cost_center,description,processing_status,rejection_reason,error_message,created_by,created_at,last_changed_by,last_changed_at
```

Create at least five valid invoices.

Use fictional vendors such as:

```text
Alpine Office Supplies GmbH
Northstar Cloud Services Ltd
Rhine Logistics GmbH
Baltic Software Consulting UG
Munich Mobility Parts GmbH
```

Create invalid records covering:

* Missing vendor ID
* Missing invoice number
* Zero gross amount
* Negative tax amount
* Unsupported currency
* Amount reconciliation failure
* Rejected invoice without rejection reason
* Invalid status

Create duplicate data where two rows have the same:

```text
vendor_id + invoice_number
```

Do not use real company financial records.

## Reporting

Create a finance summary service.

It should calculate:

* Total invoice count
* Count by status
* Gross amount by currency
* Approved gross amount by currency
* Posted gross amount by currency
* Rejected invoice count
* Validation error count
* Vendor count
* Average gross amount by currency

Never combine different currencies into one financial total.

Return a serializable dictionary.

## SAP OData client

Create a client class prepared for future SAP integration.

It should support method signatures equivalent to:

```python
list_invoices()
get_invoice(invoice_uuid)
create_invoice(invoice)
update_invoice(invoice)
execute_action(invoice_uuid, action_name, parameters=None)
```

Configuration must use environment variables:

```text
SAP_ODATA_URL
SAP_USERNAME
SAP_PASSWORD
SAP_VERIFY_SSL
```

Create `.env.example`.

Do not commit real credentials.

The client must:

* Use timeouts
* Call `raise_for_status()`
* Handle invalid JSON
* Raise clear custom exceptions
* Avoid printing credentials
* Avoid logging authorization headers

The tests must mock HTTP calls. They must not require a real SAP service.

## Command-line interface

Create a CLI that can run with a module command similar to:

```powershell
python -m sap_finance_extension.cli --help
```

Commands:

```text
init
import-csv
list
show
validate
approve
reject
reopen
post
summary
```

Examples:

```powershell
python -m sap_finance_extension.cli init

python -m sap_finance_extension.cli import-csv `
  sample-data/valid_invoices.csv

python -m sap_finance_extension.cli list

python -m sap_finance_extension.cli summary
```

Use clear terminal output.

Return non-zero exit codes for failed commands.

## Tests

Use pytest.

Create tests for:

### Validation

* Valid invoice passes
* Missing vendor ID fails
* Missing invoice number fails
* Gross amount of zero fails
* Negative tax fails
* Unsupported currency fails
* Amount reconciliation failure fails
* Duplicate vendor and invoice number fails

### Lifecycle

* New invoice can be validated
* New invoice cannot be approved
* Validated invoice can be approved
* Validated invoice can be rejected
* Rejection requires a reason
* Rejected invoice can be reopened
* Approved invoice can be posted
* Rejected invoice cannot be posted
* Posted invoice cannot be modified

### Repository

* Add invoice
* Retrieve invoice
* Update invoice
* Reject duplicate UUID
* Find by vendor and invoice number
* Delete invoice
* Persistence survives repository reinitialization

### CSV loader

* Valid file imports
* Invalid rows are reported
* Missing headers are reported
* Decimal parsing works
* Date parsing works
* Invalid status is reported

### Reporting

* Counts by status are correct
* Currency totals remain separate
* Approved totals are correct
* Posted totals are correct
* Average values are correct

Aim for at least:

```text
85% test coverage
```

## ABAP source drafts

Use the prefix:

```text
ZNA_
```

Suggested objects:

```text
ZNA_FINANCE
ZNA_INVOICE
ZNA_I_INVOICE
ZNA_C_INVOICE
ZNA_BP_INVOICE
ZNA_SD_INVOICE
ZNA_UI_INVOICE_O4
ZNA_CL_INVOICE_VALIDATOR
ZNA_CL_INVOICE_DATA
```

Create readable ABAP Cloud-oriented drafts for:

* Database table
* CDS interface view
* CDS projection view
* Managed RAP behavior definition
* Behavior implementation class
* Validation helper class
* Sample-data helper class
* Service definition
* ABAP Unit test draft

Include comments stating:

```text
This source must be imported, adjusted where required, compiled, and activated in an SAP BTP ABAP Environment before it can be described as working SAP code.
```

The ABAP drafts should reflect:

* Required-field validation
* Amount reconciliation
* Duplicate checking
* Approve action
* Reject action
* Mark-as-posted action
* Status-transition controls
* Clean separation of validation logic

Do not invent a service-binding XML format if it cannot be represented reliably. Instead, create:

```text
abap/services/zna_ui_invoice_o4.README.md
```

Explain the manual steps for creating an OData V4 UI service binding in Eclipse ADT.

## Documentation requirements

### README.md

Create a polished project README with:

1. Project overview
2. Status
3. Business problem
4. Solution
5. Architecture
6. Invoice lifecycle
7. Features
8. Data model
9. Business rules
10. Technology stack
11. Repository structure
12. Local setup
13. CLI usage
14. Tests
15. SAP setup status
16. Clean Core approach
17. Screenshots section
18. Current limitations
19. Roadmap
20. Learning objectives
21. Author
22. License
23. Disclaimer

Include badges only when accurate.

Do not add fake build or coverage badges.

### Architecture documentation

Explain:

```text
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
```

Clearly distinguish:

* Working local components
* Draft SAP components
* Future SAP trial deployment

### Clean Core documentation

Explain:

* No modification of SAP standard objects
* Custom namespace
* Released APIs where available
* Side-by-side integration
* Modular custom logic
* Upgrade-safe extension principles
* Clear boundary between local integration and SAP core

### SAP setup documentation

Create a manual checklist for:

* SAP account
* SAP BTP trial
* ABAP Environment trial
* Eclipse installation
* ABAP Development Tools installation
* ABAP Cloud project creation
* `ZNA_FINANCE` package creation
* Importing source objects
* Activating objects
* Creating service binding
* Previewing the Fiori Elements app
* Capturing genuine screenshots

Do not claim these steps are completed.

## Mermaid diagrams

Create valid Mermaid source files.

### System architecture

Include:

* External source
* Python client
* Future OData service
* SAP BTP ABAP Environment
* Database table
* CDS
* RAP
* Fiori Elements
* Reporting client

### Lifecycle

Represent all allowed invoice status transitions.

### Data model

Show the main invoice entity and important fields.

## Security requirements

Never commit:

* Passwords
* Tokens
* Real SAP URLs
* Private keys
* Certificates
* Real supplier data
* Real invoice data
* Personal financial information

Add these patterns to `.gitignore`:

```text
.env
.env.*
!.env.example
local-data/
credentials/
private/
*.key
*.pem
*.p12
*.pfx
*.crt
__pycache__/
.pytest_cache/
.mypy_cache/
.ruff_cache/
.coverage
htmlcov/
.venv/
venv/
dist/
build/
*.egg-info/
.vscode/
.idea/
.DS_Store
Thumbs.db
```

## README disclaimer

Include:

```text
This is an independent educational portfolio project. It is not
affiliated with, endorsed by, or developed on behalf of SAP, FINN,
or any other company. SAP product names and trademarks belong to
their respective owners.
```

## Author section

Use:

```text
Noor Ahmed Shaikh
```

Links:

```text
LinkedIn: https://www.linkedin.com/in/noor-ahmedd/
GitHub: https://github.com/Noor-Ahmed-12
Portfolio: https://noorahmedshaikh.vercel.app/
```

## Local setup

Provide Windows PowerShell instructions.

Example:

```powershell
git clone https://github.com/Noor-Ahmed-12/sap-btp-abap-finance-process-extension.git
cd sap-btp-abap-finance-process-extension

python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt

$env:PYTHONPATH="$PWD\python-client\src"

pytest
python -m sap_finance_extension.cli --help
```

Also make the project work before it is pushed to GitHub.

## Quality checks

Configure and run:

```powershell
ruff check .
mypy python-client/src
pytest --cov=python-client/src --cov-report=term-missing
```

Fix errors rather than suppressing them without explanation.

## Acceptance criteria

The Codex task is complete only when:

* The full repository structure exists
* The README is complete
* Documentation files contain meaningful content
* Mermaid files are valid
* Valid sample data exists
* Invalid sample data exists
* Duplicate sample data exists
* Python models use Decimal for money
* Validation rules are implemented
* Lifecycle transitions are implemented
* Local JSON persistence works
* CSV import works
* Summary reporting works
* The CLI works
* Tests pass
* Ruff passes
* Mypy passes, or remaining limitations are clearly documented
* Coverage is at least 85%
* ABAP draft sources exist
* ABAP files are clearly labelled unverified
* SAP setup instructions are included
* No credentials exist in the repository
* No fake deployment claims exist
* No fake screenshots exist

## Work sequence

Follow this order:

1. Create the repository directory.
2. Create the folder structure.
3. Create Python packaging and configuration.
4. Implement the invoice model and enum.
5. Implement exceptions.
6. Implement validation.
7. Implement lifecycle transitions.
8. Implement local repository.
9. Implement CSV loading.
10. Implement reporting.
11. Implement the SAP OData client.
12. Implement the CLI.
13. Create sample data.
14. Write tests.
15. Run tests and quality checks.
16. Fix all discovered issues.
17. Create documentation.
18. Create Mermaid diagrams.
19. Add ABAP draft objects.
20. Review the README against the real project status.
21. Print the final repository tree.
22. Print commands for running the application and tests.
23. Summarize anything that still requires manual SAP work.

## Suggested first commit

After successful local verification, prepare the repository for this commit:

```text
Initialize SAP BTP ABAP finance process extension
```

Do not commit automatically unless Git is configured and permission is clear.

## Final Codex response

At the end, report:

* Files created
* Features implemented
* Tests run
* Test results
* Coverage result
* Lint result
* Type-checking result
* Local CLI commands
* Remaining manual SAP steps
* Any assumptions
* Any parts not completed

Start building the project now. Do not stop after creating only documentation. The local Python workflow, tests, sample data, and CLI must be functional.
