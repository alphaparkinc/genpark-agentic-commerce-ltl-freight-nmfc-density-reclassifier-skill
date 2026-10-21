# -*- coding: utf-8 -*-
"""LTL Freight NMFC Density Reclassifier for GenPark Agentic Commerce."""
import json
from typing import Dict, Any

class LTLFreightNMFCDensityReclassifier:
    @staticmethod
    def calculate_freight_density_and_nmfc_class(length_inches: float, width_inches: float, height_inches: float, weight_lbs: float) -> Dict[str, Any]:
        cubic_feet = round((length_inches * width_inches * height_inches) / 1728.0, 2)
        pcf = round(weight_lbs / max(0.1, cubic_feet), 2)
        
        # Standard 11-tier density matrix
        if pcf < 1.0: nmfc = 500
        elif pcf < 2.0: nmfc = 400
        elif pcf < 4.0: nmfc = 300
        elif pcf < 6.0: nmfc = 250
        elif pcf < 8.0: nmfc = 175
        elif pcf < 10.0: nmfc = 125
        elif pcf < 12.0: nmfc = 100
        elif pcf < 15.0: nmfc = 85
        elif pcf < 22.5: nmfc = 70
        elif pcf < 30.0: nmfc = 65
        else: nmfc = 50
        
        return {
            "cubic_feet": cubic_feet,
            "weight_lbs": weight_lbs,
            "pounds_per_cubic_foot_pcf": pcf,
            "eligible_nmfc_class": nmfc,
            "freight_rating_efficiency": "HIGH_DENSITY_FAVORABLE" if nmfc <= 70 else "LOW_DENSITY_CUBE_PENALTY"
        }

    @staticmethod
    def audit_carrier_w_and_r_chargeback(carrier_billed_class: int, actual_verified_class: int, billed_rate_usd: float, fuel_surcharge_pct: float = 24.5) -> Dict[str, Any]:
        is_overcharged = carrier_billed_class > actual_verified_class
        class_spread = max(0, carrier_billed_class - actual_verified_class)
        rate_diff_factor = (class_spread / 100.0) * 0.18
        disputed_base_usd = round(billed_rate_usd * rate_diff_factor, 2)
        disputed_fuel_usd = round(disputed_base_usd * (fuel_surcharge_pct / 100.0), 2)
        total_claim_usd = round(disputed_base_usd + disputed_fuel_usd, 2)
        
        return {
            "carrier_billed_class": carrier_billed_class,
            "verified_shipper_class": actual_verified_class,
            "overcharge_detected": is_overcharged,
            "total_reclaimable_dispute_usd": total_claim_usd,
            "dispute_action": "GENERATE_STANDARD_FREIGHT_CLAIM_PACKET" if is_overcharged else "NO_DISPUTE_VALID_RATING"
        }
