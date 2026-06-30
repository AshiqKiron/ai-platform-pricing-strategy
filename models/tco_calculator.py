# models/tco_calculator.py
import pandas as pd
import os

def calculate_tco():
    # --- ASSUMPTIONS ---
    num_gpus = 100
    training_hours = 720  # 1 month of continuous training
    on_demand_price = 2.50    # $/GPU/hr (Legacy baseline)
    raw_spot_price = 0.80     # $/GPU/hr (Raw spot baseline)
    managed_spot_price = 1.00 # $/GPU/hr (Our Tier 3 price: 25% premium over raw spot)
    
    # Overhead assumptions
    on_demand_idle_waste_pct = 0.20  # 20% of on-demand time is idle/waiting for data
    raw_spot_interruption_overhead = 0.15 # 15% of time lost to spot interruptions + manual restarts
    manual_spot_eng_overhead = 6000  # $6,000 engineering cost to manage raw spot failures

    # --- CALCULATIONS ---
    
    # 1. Legacy On-Demand
    legacy_ondemand_compute = num_gpus * training_hours * on_demand_price
    legacy_ondemand_waste = legacy_ondemand_compute * on_demand_idle_waste_pct
    legacy_ondemand_tco = legacy_ondemand_compute # Waste is baked into the high hourly rate

    # 2. Legacy Raw Spot (Manual Management)
    # Because of interruptions, they have to pay for more hours to get the same useful compute
    raw_spot_effective_hours = training_hours / (1 - raw_spot_interruption_overhead)
    legacy_rawspot_compute = num_gpus * raw_spot_effective_hours * raw_spot_price
    legacy_rawspot_tco = legacy_rawspot_compute + manual_spot_eng_overhead

    # 3. Proposed Managed Spot (Tier 3)
    # Automated checkpointing means 0% wasted time. They only pay for exact useful hours.
    proposed_managed_compute = num_gpus * training_hours * managed_spot_price
    proposed_managed_tco = proposed_managed_compute

    # --- ROI / SAVINGS ---
    savings_vs_ondemand = legacy_ondemand_tco - proposed_managed_tco
    savings_pct = (savings_vs_ondemand / legacy_ondemand_tco) * 100

    # --- GENERATE OUTPUT ---
    data = {
        'Pricing Model': [
            'Legacy On-Demand', 
            'Legacy Raw Spot (Manual Mgmt)', 
            'Proposed Managed Spot (Tier 3)'
        ],
        'Base Price ($/GPU/hr)': [on_demand_price, raw_spot_price, managed_spot_price],
        'Total GPU Hours Billed': [
            num_gpus * training_hours, 
            num_gpus * raw_spot_effective_hours, 
            num_gpus * training_hours
        ],
        'Compute Cost ($)': [
            legacy_ondemand_compute, 
            legacy_rawspot_compute, 
            proposed_managed_compute
        ],
        'Hidden Costs/Waste ($)': [
            legacy_ondemand_waste, 
            manual_spot_eng_overhead, 
            0
        ],
        'Total TCO ($)': [
            legacy_ondemand_tco, 
            legacy_rawspot_tco, 
            proposed_managed_tco
        ]
    }
    
    df = pd.DataFrame(data)
    
    # Save to CSV
    os.makedirs('../outputs', exist_ok=True)
    df.to_csv('../outputs/tco_comparison.csv', index=False)
    
    # Print Summary
    print("--- AI PLATFORM TCO COMPARISON (100 GPUs / 1 Month) ---")
    print(df.to_string(index=False))
    print("\n--- THE 'AHA' MOMENT ---")
    print(f"By switching from Legacy On-Demand to our Managed Spot (Tier 3),")
    print(f"the customer saves ${savings_vs_ondemand:,.2f} per month.")
    print(f"This represents a {savings_pct:.1f}% reduction in Training TCO!")
    print("\nCSV saved to: ../outputs/tco_comparison.csv")

if __name__ == "__main__":
    calculate_tco()