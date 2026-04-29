from engine.calc import calculate_bill

def compare_two_tariffs(t1, t2, usage_kwh, peak_kw, billing_days, rider, tax):
    return {
        'tariff_a': calculate_bill(t1, usage_kwh, peak_kw, billing_days, rider, tax),
        'tariff_b': calculate_bill(t2, usage_kwh, peak_kw, billing_days, rider, tax)
    }

def find_lowest_cost_tariff(tariffs, usage_kwh, peak_kw, billing_days, rider, tax):
    results = []
    for t in tariffs:
        min_kw = t['eligibility']['min_kw']
        max_kw = t['eligibility']['max_kw']
        if peak_kw < min_kw:
            continue
        if max_kw is not None and peak_kw > max_kw:
            continue
        bill = calculate_bill(t, usage_kwh, peak_kw, billing_days, rider, tax)
        results.append((t['tariff'], bill['total']))
    return sorted(results, key=lambda x: x[1])
