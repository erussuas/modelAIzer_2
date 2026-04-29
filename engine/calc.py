def calculate_bill(tariff, usage_kwh, peak_kw, billing_days, rider, tax):
    items = []
    subtotal = 0.0

    cust = billing_days * tariff['customer_charge_per_day']
    subtotal += cust
    items.append({'name': 'Customer Charge', 'amount': round(cust, 2)})

    total_kwh = 0.0
    for p, kwh in usage_kwh.items():
        rate = tariff['energy_rates'].get(p, 0)
        charge = kwh * rate
        total_kwh += kwh
        subtotal += charge
        items.append({'name': f'Energy {p}', 'amount': round(charge, 2)})

    if tariff.get('has_demand'):
        d_rate = tariff['demand_rates']['billing_demand']
        d_charge = peak_kw * d_rate
        subtotal += d_charge
        items.append({'name': 'Demand Charge', 'amount': round(d_charge, 2)})

    rider_charge = total_kwh * rider
    subtotal += rider_charge
    items.append({'name': 'Riders', 'amount': round(rider_charge, 2)})

    tax_amt = subtotal * tax
    return {
        'tariff': tariff['tariff'],
        'line_items': items,
        'subtotal': round(subtotal, 2),
        'tax': round(tax_amt, 2),
        'total': round(subtotal + tax_amt, 2)
    }
