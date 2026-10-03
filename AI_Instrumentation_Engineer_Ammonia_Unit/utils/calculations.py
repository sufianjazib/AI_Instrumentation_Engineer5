def percent_deviation(actual, reference):
    if reference == 0:
        return 0.0
    return abs(actual - reference) / abs(reference) * 100.0
