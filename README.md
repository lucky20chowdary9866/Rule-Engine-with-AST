# Rule Engine with AST

## Overview.
This project is a rule engine that uses Abstract Syntax Trees (AST) to represent, develop, and analyze complicated rules for assessing user eligibility based on age, department, salary, and experience.
## Outline Project Features
- Generate dynamic eligibility rules based on user traits.
- Combine many rules into one AST.
- Check user data against regulations to ensure eligibility.
- Supports AND/OR operators and numerous conditions.
- API endpoints for rule generation, combination, and evaluation.
### Prerequisites
- Python 3.x
## API Endpoints.

- **GET /create_rule**: Generate a new rule using a rule string. The rule string should be specified as a query parameter.
- **GET /combine_rules**: Combine several rules into a single AST. Rules should be specified as query parameters.
- **GET /evaluate_rule**: Test a rule with user data. The rule ID and user data should be used as query parameters.
##**Testing**
-pytest
**Security Features:**
-API token-based authentication.
-Input validation for rules and data.
**Performance Optimizations**
-Rule caching enables speedier evaluations.
-Optimized AST traversal.
**Error Handling**
-Descriptive error messages for faulty rules and missing data
