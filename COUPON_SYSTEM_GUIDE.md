# 🎫 Coupon System Quick Reference

## Available Coupons

### 1. NEWYEAR50
- **Discount:** 50% OFF
- **Valid:** January 1-31, 2025
- **Usage:** Any feature, any user
- **Max Uses:** 1000 total
- **Example:** ₹100 → ₹50

### 2. WEEKEND75
- **Discount:** 75% OFF
- **Valid:** Saturdays & Sundays only
- **Usage:** Any feature, any user
- **Max Uses:** 500 total
- **Example:** ₹100 → ₹25

### 3. FIRST50
- **Discount:** 50% OFF
- **Valid:** Anytime
- **Usage:** First purchase only
- **Max Uses:** Unlimited
- **Example:** ₹100 → ₹50

### 4. PREMIUM25
- **Discount:** 25% OFF
- **Valid:** Anytime
- **Usage:** Matchmaking, Varshaphal, Dasha Detail only
- **Max Uses:** Unlimited
- **Example:** ₹100 → ₹75

---

## How to Use Coupons

### For Credit Purchase
1. Go to "Buy Credits" page
2. Select a credit pack
3. View active coupons displayed
4. Enter coupon code in the input box
5. Click "Apply" button
6. See discounted price
7. Pay the new amount
8. Transaction complete!

### For Direct Feature Usage
Coupons are applied during credit purchase, not during feature usage. Users buy credits with discount, then use credits for features.

---

## Adding New Coupons

### Edit config.yaml
```yaml
payment:
  coupons:
    enabled: true
    codes:
      - code: "YOUR_CODE"
        discount_percent: 50
        valid_from: "2025-02-01"
        valid_until: "2025-02-28"
        description: "February Special"
        max_uses: 500
```

### Coupon Properties

**Required:**
- `code`: Unique coupon code (uppercase recommended)
- `discount_percent`: 1-100

**Optional:**
- `valid_from`: "YYYY-MM-DD" format
- `valid_until`: "YYYY-MM-DD" format
- `valid_days`: ["Monday", "Tuesday", etc.]
- `description`: User-friendly description
- `max_uses`: Total usage limit (null = unlimited)
- `first_purchase_only`: true/false
- `features`: ["matchmaking", "varshaphal", etc.]

---

## Validation Rules

### Date-based
```yaml
valid_from: "2025-01-01"
valid_until: "2025-01-31"
```
Coupon only works between these dates.

### Day-based
```yaml
valid_days: ["Saturday", "Sunday"]
```
Coupon only works on weekends.

### First Purchase
```yaml
first_purchase_only: true
```
Only for users with no prior transactions.

### Feature-specific
```yaml
features: ["matchmaking", "varshaphal", "dasha_detail"]
```
Only for specific premium features.

### Usage Limits
```yaml
max_uses: 1000
```
Stops working after 1000 total uses.

---

## Error Messages

| Error | Reason |
|-------|--------|
| "Invalid coupon code" | Code doesn't exist |
| "Coupon usage limit reached" | Max uses exceeded |
| "This coupon is only valid for first purchase" | User has prior transactions |
| "Coupon valid from YYYY-MM-DD" | Not yet active |
| "Coupon expired" | Past expiry date |
| "Coupon valid only on: Sat, Sun" | Wrong day of week |
| "Coupon valid only for: matchmaking, varshaphal" | Feature not included |

---

## Backend Files

### Coupon Data Storage
**File:** `data/payments/coupon_usage.json`

**Structure:**
```json
{
  "NEWYEAR50": {
    "total_uses": 250,
    "users": {
      "user@example.com": [
        {
          "timestamp": "2025-01-15T10:30:00",
          "feature": null,
          "original_price": 100,
          "discount_percent": 50,
          "final_price": 50
        }
      ]
    }
  }
}
```

### Payment Manager Methods

**validate_coupon(code, email, feature)**
- Returns: (is_valid, message, discount_percent)
- Checks all validation rules

**apply_coupon(code, email, original_price, feature)**
- Returns: (success, final_price, message)
- Calculates discount and tracks usage

**get_active_coupons()**
- Returns: List of currently active coupons
- Filters by date, usage limits

---

## Usage Scenarios

### Scenario 1: Weekend Sale
```yaml
code: "WEEKEND75"
discount_percent: 75
valid_days: ["Saturday", "Sunday"]
description: "Weekend Bonanza - 75% off"
```

**Customer buys on Saturday:**
- Selects ₹80 pack (10 credits)
- Applies WEEKEND75
- Pays ₹20 (75% off)
- Gets 10 credits

### Scenario 2: New Year Campaign
```yaml
code: "NEWYEAR50"
discount_percent: 50
valid_from: "2025-01-01"
valid_until: "2025-01-31"
max_uses: 1000
```

**Customer buys on Jan 15:**
- Selects ₹120 pack (15 credits)
- Applies NEWYEAR50
- Pays ₹60 (50% off)
- Gets 15 credits

### Scenario 3: First Time Buyer
```yaml
code: "FIRST50"
discount_percent: 50
first_purchase_only: true
```

**New customer:**
- Selects ₹40 pack (5 credits)
- Applies FIRST50
- Pays ₹20 (50% off)
- Gets 5 credits

**Returning customer:**
- Tries FIRST50
- Gets error: "Only valid for first purchase"

### Scenario 4: Premium Feature Promo
```yaml
code: "PREMIUM25"
discount_percent: 25
features: ["matchmaking", "varshaphal", "dasha_detail"]
```

**For premium features (100 credits):**
- Uses PREMIUM25
- Saves 25 credits
- Pays 75 credits instead of 100

---

## Admin Tasks

### View Coupon Statistics
```python
# In Python console
from src.payment.payment_manager import PaymentManager
pm = PaymentManager(config=config)

# Get active coupons
coupons = pm.get_active_coupons()
print(coupons)

# Check specific coupon usage
usage = pm.coupon_usage.get('NEWYEAR50', {})
print(f"Total uses: {usage.get('total_uses', 0)}")
```

### Disable a Coupon
In `config.yaml`, set `max_uses` to current usage count:
```yaml
- code: "NEWYEAR50"
  max_uses: 250  # Set to current usage to stop
```

### Create Limited Time Offer
```yaml
- code: "FLASH90"
  discount_percent: 90
  valid_from: "2025-01-20"
  valid_until: "2025-01-20"  # Same day only!
  max_uses: 100
  description: "24-Hour Flash Sale - 90% off!"
```

---

## Best Practices

1. **Test coupons** before announcing
2. **Set reasonable max_uses** to control costs
3. **Use descriptive codes** (NEWYEAR50 vs ABC123)
4. **Monitor usage** regularly
5. **Expire old coupons** to keep config clean
6. **Combine restrictions** (date + feature + first purchase)
7. **Announce coupons** clearly to users
8. **Track ROI** to optimize discounts

---

## Troubleshooting

### Coupon not working?
1. Check config.yaml syntax (valid YAML)
2. Verify code spelling (case-sensitive)
3. Check current date/day
4. Verify max_uses not exceeded
5. Restart app after config changes

### Discount not applied?
1. Ensure payment manager initialized with config
2. Check apply_coupon() return value
3. Verify coupon_usage.json permissions
4. Check for error messages in UI

---

## Future Enhancements

1. **Auto-apply best coupon** for user
2. **Stackable coupons** (multiple discounts)
3. **User-specific coupons** (loyalty rewards)
4. **Referral codes** (friend invites)
5. **Birthday coupons** (automatic generation)
6. **Email notifications** for new coupons
7. **Push notifications** for expiring coupons
8. **A/B testing** for discount percentages

---

## Contact

For questions about the coupon system:
- Check `FEATURES_COMPLETED.md` for implementation details
- Review `src/payment/payment_manager.py` for code
- Edit `config/config.yaml` to add/modify coupons

**Happy Discounting!** 🎉
