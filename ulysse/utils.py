def _generate_score_key(column_name, column_value):
    """Generate a unique key from column name/value pair for Redis."""
    return 'score' + column_name + column_value
