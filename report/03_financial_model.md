# The Financial Model: Proving the TCO Reduction

To prove the value of Tier 3 (Managed Spot), we modeled a hypothetical enterprise customer running a 100-GPU training cluster for one month (720 hours).

## The Scenarios
1. **Legacy On-Demand:** Customer pays premium hourly rates. 20% of that time is wasted due to pipeline idle time.
2. **Legacy Raw Spot (Manual):** Customer uses cheap raw spot instances, but loses 15% of compute time to interruptions. They must manually manage restarts, costing $6,000 in engineering overhead.
3. **Proposed Managed Spot (Tier 3):** Customer pays a slight premium over raw spot, but our automated checkpointing ensures 100% useful compute time and zero engineering overhead.

## The "Aha" Spreadsheet Results
*(Run `models/tco_calculator.py` to generate the exact CSV data)*

| Pricing Model | Base Price ($/GPU/hr) | Total TCO ($) |
| :--- | :--- | :--- |
| Legacy On-Demand | $2.50 | $180,000 |
| Legacy Raw Spot (Manual) | $0.80 | $65,882 |
| **Proposed Managed Spot** | **$1.00** | **$72,000** |

## The Takeaway
While Raw Spot looks cheaper on a spreadsheet, the hidden costs of manual management and interruptions make it risky. Our Managed Spot model guarantees the training finishes on time while delivering a **60% reduction in TCO** compared to standard On-Demand pricing. We sell *reliability and efficiency*, not just raw silicon.