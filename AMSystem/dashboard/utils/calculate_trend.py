def calculate_trend(current, previous):
    """Calculate percentage change between current and previous values."""
    if previous > 0:
        return round(((current - previous) / previous) * 100, 1)
    return 100 if current > 0 else 0
