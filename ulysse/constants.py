# TODO: Find more pertinent default columns to load?
DEFAULT_COLUMNS = [
    'SIREN', 'NIC', 'L1_NORMALISEE', 'TEFET', 'DEFET', 'DEPCOMEN',
    'APEN700', 'CATEGORIE', 'DATEMAJ'
]

# Attempt to exclude raw text column from indexation.
# Note that it works with suffixes, e.g.: `L1_NORMALISEE`
# will be excluded because `NORMALISEE` is part of the list.
DEFAULT_EXCLUDED_COLUMNS = [
    'NORMALISEE', 'DECLAREE', 'ENSEIGNE', 'LIBNATETAB', 'LIBAPET',
    'LIBTEFET', 'NOMEN_LONG', 'LIBNJ', 'LIBAPEN', 'LIBTEFEN'
]
