SUBTYPE_CATEGORIES = (
    ('akcesoria_eti', 'ETI - Radość Szycia'),
    ('hafciarka_z_programem', 'Hafciarka + program'),
    ('hafciarka', 'Hafciarka'),
    ('igly', 'Igły'),
    ('inne', 'Inne'),
    ('nici', 'Nici'),
    ('maszyna_wieloczynnosciowa', 'Maszyna wieloczynnościowa'),
    ('nozyczki', 'Nożyczki'),
    ('owerlok', 'Owerlok/Coverlok'),
    ('programy', 'Programy'),
    ('silniki', 'Silniki'),
    ('stabilizatory', 'Stabilizatory'),
    ('wykroje', 'Wykroje'),
    ('zestawy_akcesoriow', 'Zestawy akcesoriów'),
    ('zarowki', 'Żarówki')
)

TYPE_CATEGORIES = (
    ('akcesoria', 'Akcesoria'),
    ('maszyny', 'Maszyny'),
    ('zestawy', 'Zestawy')
)

def fill_manufacturer(code):
    value = code.split(' ')[0]
    codes = {'JANOME': 'Janome',
             'ELNA': 'Elna',
             'JUNO': 'Juno by Janome',
             'FISKARS': 'Fiskars',
             'MADEIRA': 'Madeira',
             'ETI': 'Eti'}
    if value in codes.keys():
        manufacturer = codes[value]
    else:
        manufacturer = ''
    return manufacturer


def fill_type(mark):
    # 77 to "M" w symfonii
    if int(mark) == 77:
        type = 'maszyny'
    else:
        type = 'akcesoria'
    return type


def fill_sub_type(manufacturer, mark, code):
    # 70 to "F"
    # 77 to "M" w symfonii
    mark = int(mark)
    if manufacturer == 'Fiskars' and mark == 70:
        sub_type = 'nożyczki'
        is_active = True
    elif mark == 77:
        sub_type = ''
        is_active = True
    elif mark == '':
        sub_type = ''
        is_active = False
    elif manufacturer == 'Madeira':
        is_active = True
        if 'KOLOR' in code:
            sub_type = 'nici'
        else:
            sub_type = 'stabilizatory'
    else:
        sub_type = ''
        is_active = True
    return sub_type, is_active


def fill_category(code, mark=''):
    mark = int(mark)
    manufacturer = fill_manufacturer(code)
    type = fill_type(mark)
    sub_type, is_active = fill_sub_type(manufacturer, mark, code)

    return manufacturer, type, sub_type, is_active