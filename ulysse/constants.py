# TODO: Find more pertinent default columns to load?
DEFAULT_COLUMNS = [
    'SIREN', 'NIC', 'L1_NORMALISEE', 'TEFET', 'DEFET', 'DEPCOMEN',
    'APEN700', 'CATEGORIE', 'DCREN', 'DATEMAJ'
]

# TODO: Find more pertinent default columns to load?
DEFAULT_UPDATE_COLUMNS = ['VMAJ', 'DATEMAJ', 'EVE', 'DATEVE']

# Attempt to exclude raw text column from indexation.
# Note that it works with suffixes, e.g.: `L1_NORMALISEE`
# will be excluded because `NORMALISEE` is part of the list.
DEFAULT_EXCLUDED_COLUMNS = [
    'NORMALISEE', 'DECLAREE', 'ENSEIGNE', 'LIBNATETAB', 'LIBAPET',
    'LIBTEFET', 'NOMEN_LONG', 'LIBNJ', 'LIBAPEN', 'LIBTEFEN'
]

# Beware: `DATEMAJ` is also in the stock file, which is not documented.
# That's why we removed it from that list.
UPDATE_COLUMNS = [
    'VMAJ', 'VMAJ1', 'VMAJ2', 'VMAJ3', 'EVE', 'DATEVE', 'TYPCREH',
    'DREACTET', 'DREACTEN', 'MADRESSE', 'MENSEIGNE', 'MAPET', 'MPRODET',
    'MAUXILT', 'MNOMEN', 'MSIGLE', 'MNICSIEGE', 'MNJ', 'MAPEN', 'MPRODEN',
    'SIRETPS', 'TEL'
]
