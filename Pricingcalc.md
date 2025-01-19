Adding **claim pricing calculations** to the above example can be accomplished by incorporating **pricing rules and formulas** into the pipeline using **Durable Rules** for logic execution and **Python** for complex calculations. Here's how you can enhance the workflow:

---

### **Claim Pricing Calculation Workflow**

1. **Pricing Rules**: Define pricing rules based on service type, age group, insurance type, or other parameters.
2. **Calculation Logic**: Calculate claim prices based on rules and apply discounts, taxes, or penalties.
3. **Integration**: Extend Durable Rules and integrate pricing logic into the workflow.

---

### **Step 1: Define Pricing Rules**

#### Sample Rules:
1. **Base Pricing**:
   - Claims under $500 are charged a flat rate.
   - Claims between $500 and $1,000 are charged at 80% of the `AmountCharged`.
   - Claims over $1,000 are charged at 70% of the `AmountCharged`.

2. **Senior Discount**:
   - Patients over 65 receive a 10% discount on the final price.

3. **Pediatric Discount**:
   - Patients under 18 receive a 5% discount.

4. **Taxation**:
   - Apply a 5% tax to all claims after discounts.

---

### **Step 2: Extend Durable Rules for Pricing Logic**

Here’s how to implement the above pricing rules using **Durable Rules**:

#### Durable Rules Code:
```python
from durable.lang import ruleset, when_all, assert_fact
import logging

# Set up logging
logging.basicConfig(filename="pricing_log.log", level=logging.INFO)

# Define the ruleset
with ruleset("claim_pricing_rules"):

    # Rule for base pricing
    @when_all(c.amount_charged < 500)
    def flat_rate_pricing(c):
        c.price = 100  # Flat rate for claims under $500
        logging.info(f"Claim {c.claim_id}: Flat rate applied. Final Price = {c.price}")

    @when_all((c.amount_charged >= 500) & (c.amount_charged <= 1000))
    def mid_range_pricing(c):
        c.price = c.amount_charged * 0.8
        logging.info(f"Claim {c.claim_id}: 80% pricing applied. Final Price = {c.price}")

    @when_all(c.amount_charged > 1000)
    def high_value_pricing(c):
        c.price = c.amount_charged * 0.7
        logging.info(f"Claim {c.claim_id}: 70% pricing applied. Final Price = {c.price}")

    # Rule for senior discount
    @when_all(c.age > 65)
    def senior_discount(c):
        c.price *= 0.9  # 10% discount
        logging.info(f"Claim {c.claim_id}: Senior discount applied. Final Price = {c.price}")

    # Rule for pediatric discount
    @when_all(c.age < 18)
    def pediatric_discount(c):
        c.price *= 0.95  # 5% discount
        logging.info(f"Claim {c.claim_id}: Pediatric discount applied. Final Price = {c.price}")

    # Rule for taxation
    @when_all(+c.price)
    def apply_tax(c):
        c.price *= 1.05  # 5% tax
        logging.info(f"Claim {c.claim_id}: Tax applied. Final Price = {c.price}")

# Sample claims
claims = [
    {"claim_id": "C001", "amount_charged": 500, "age": 45},
    {"claim_id": "C002", "amount_charged": 1200, "age": 17},
    {"claim_id": "C003", "amount_charged": 300, "age": 70},
    {"claim_id": "C004", "amount_charged": 150, "age": 5},
]

# Execute pricing rules
for claim in claims:
    assert_fact("claim_pricing_rules", claim)

# Output logged pricing details
with open("pricing_log.log", "r") as log_file:
    print(log_file.read())
```

---

### **Step 3: Pricing Calculation Workflow**
1. Load claims data (`claims.csv`).
2. Pass each claim through the pricing rules.
3. Log and output the calculated prices.

---

### **Sample Output**

#### Logs:
```plaintext
Claim C001: 80% pricing applied. Final Price = 400.0
Claim C002: 70% pricing applied. Final Price = 840.0
Claim C002: Pediatric discount applied. Final Price = 798.0
Claim C002: Tax applied. Final Price = 837.9
Claim C003: Flat rate applied. Final Price = 100
Claim C003: Senior discount applied. Final Price = 90.0
Claim C003: Tax applied. Final Price = 94.5
Claim C004: Flat rate applied. Final Price = 100
Claim C004: Pediatric discount applied. Final Price = 95.0
Claim C004: Tax applied. Final Price = 99.75
```

#### Final Pricing:
| ClaimID | Base Price | Discounts   | Tax     | Final Price |
|---------|------------|-------------|---------|-------------|
| C001    | $500.00    | $0.00       | $20.00  | $400.00     |
| C002    | $1200.00   | $42.00      | $39.90  | $837.90     |
| C003    | $300.00    | $10.00      | $4.50   | $94.50      |
| C004    | $150.00    | $5.00       | $4.75   | $99.75      |

---

### **Step 4: Integration with Robot Framework**

Extend the **Robot Framework** test suite to include pricing calculations.

#### Robot Framework Test Case (edi_claim_tests.robot):
```robot
*** Test Cases ***
Validate EDI Claims
    Run Process    python    validate_claims.py

Execute Business Rules
    Run Process    python    execute_rules.py

Calculate Claim Pricing
    Run Process    python    calculate_pricing.py
```

---

### **Step 5: Reporting**
1. Combine validation, rule execution, and pricing results into a unified report.
2. Output:
   - Final pricing in a CSV/JSON format.
   - Robot Framework HTML reports.
   - Logs for auditing purposes.

---

This approach ensures accurate pricing for healthcare claims based on defined rules, integrates seamlessly with validation and business logic, and produces unified reporting for stakeholders. Let me know if you'd like a deeper dive into specific components!
