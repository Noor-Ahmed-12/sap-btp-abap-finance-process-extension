# Business rules

The local Python application implements the following rules:

1. Invoice UUID must be unique.
2. Company code is required.
3. Vendor ID is required.
4. Vendor name is required.
5. Invoice number is required.
6. Invoice date is required.
7. Currency must be one of EUR, USD, GBP, CHF.
8. Gross amount must be greater than zero.
9. Tax amount cannot be negative.
10. Net amount cannot be negative.
11. Net amount plus tax amount must equal gross amount within a tolerance of 0.01.
12. Vendor ID plus invoice number must be unique.
13. Only a NEW invoice can be validated.
14. Only a VALIDATED invoice can be approved.
15. A NEW or VALIDATED invoice can be rejected.
16. A rejected invoice requires a rejection reason.
17. Only an APPROVED invoice can be posted.
18. A posted invoice cannot be modified.
19. Validation failures return understandable messages.
