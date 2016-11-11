# TODO: Find more pertinent default columns to load?
DEFAULT_COLUMNS = [
    'SIREN', 'NIC', 'L1_NORMALISEE', 'TEFET', 'DEFET', 'DEPCOMEN',
    'APEN700', 'CATEGORIE', 'DCREN', 'DATEMAJ'
]

ALL_COLUMNS = [
    'SIREN', 'NIC', 'L1_NORMALISEE', 'L2_NORMALISEE', 'L3_NORMALISEE',
    'L4_NORMALISEE', 'L5_NORMALISEE', 'L6_NORMALISEE', 'L7_NORMALISEE',
    'L1_DECLAREE', 'L2_DECLAREE', 'L3_DECLAREE', 'L4_DECLAREE', 'L5_DECLAREE',
    'L6_DECLAREE', 'L7_DECLAREE', 'NUMVOIE', 'INDREP', 'TYPVOIE', 'LIBVOIE',
    'CODPOS', 'CEDEX', 'RPET', 'LIBREG', 'DEPET', 'ARRONET', 'CTONET', 'COMET',
    'LIBCOM', 'DU', 'TU', 'UU', 'EPCI', 'TCD', 'ZEMET', 'SIEGE', 'ENSEIGNE',
    'IND_PUBLIPO', 'DIFFCOM', 'AMINTRET', 'NATETAB', 'LIBNATETAB', 'APET700',
    'LIBAPET', 'DAPET', 'TEFET', 'LIBTEFET', 'EFETCENT', 'DEFET', 'ORIGINE',
    'DCRET', 'DDEBACT', 'ACTIVNAT', 'LIEUACT', 'ACTISURF', 'SAISONAT', 'MODET',
    'PRODET', 'PRODPART', 'AUXILT', 'NOMEN_LONG', 'SIGLE', 'NOM', 'PRENOM',
    'CIVILITE', 'RNA', 'NICSIEGE', 'RPEN', 'DEPCOMEN', 'ADR_MAIL', 'NJ',
    'LIBNJ', 'APEN700', 'LIBAPEN', 'DAPEN', 'APRM', 'ESS', 'DATEESS', 'TEFEN',
    'LIBTEFEN', 'EFENCENT', 'DEFEN', 'CATEGORIE', 'DCREN', 'AMINTREN',
    'MONOACT', 'MODEN', 'PRODEN', 'ESAANN', 'TCA', 'ESAAPEN', 'ESASEC1N',
    'ESASEC2N', 'ESASEC3N', 'ESASEC4N', 'VMAJ', 'VMAJ1', 'VMAJ2', 'VMAJ3',
    'DATEMAJ'  # <- Wrongly documented as being part of update files only.
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
ALL_UPDATE_COLUMNS = [
    'VMAJ', 'VMAJ1', 'VMAJ2', 'VMAJ3', 'EVE', 'DATEVE', 'TYPCREH',
    'DREACTET', 'DREACTEN', 'MADRESSE', 'MENSEIGNE', 'MAPET', 'MPRODET',
    'MAUXILT', 'MNOMEN', 'MSIGLE', 'MNICSIEGE', 'MNJ', 'MAPEN', 'MPRODEN',
    'SIRETPS', 'TEL'
]
