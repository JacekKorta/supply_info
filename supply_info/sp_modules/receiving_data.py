from supply_info.models import ActiveProductList, PriceList, Product, ProductAvailability
from . import products_info
"""
dane z pliku 'towary.txt'
"""

def receive_main_data(data):
    for line in data.split('\n'):
        _, code, name, _, prod_group, _, _, _, price_a, _, price_b, _, price_c, _, price_d, _, _, _, mark, *_ \
            = line.split('\t')
        code = code[1:] if code.startswith(' ') else code
        name = name[1:] if name.startswith(' ') else name
        manufacturer, type, sub_type, is_active = products_info.fill_category(code, mark)
        try:
            Product.objects.get(code=code)
            print(f'{code} already exist')
        except Product.DoesNotExist:
                prod = Product(code=code,
                               name=name[:400],
                               prod_group=prod_group,
                               mark=mark,
                               type=type,
                               sub_type=sub_type,
                               manufacturer=manufacturer)

                prod.save()
                p = PriceList(product_code=Product.objects.get(code=prod.code),
                              price_a=round(float(price_a), 2),
                              price_b=round(float(price_b), 2),
                              price_c=round(float(price_c), 2),
                              price_d=round(float(price_d), 2))
                p.save()
                if is_active:
                    a = ActiveProductList(product_code=Product.objects.get(code=prod.code, is_active=True))
                    a.save()


'''
dane z raportu: "bierzące stany i rezerwacje towarów"
'''


def receive_availability_data(data):
    for line in data.split('\n')[2:]:
        try:
            code, _, _, _, _, _, availability, *_ = line.split('\t')
        except ValueError:
            print(f'corrupted data in {line}')
        try:
            a = ProductAvailability.objects.get(product_code=Product.objects.get(code=code))
            a.availability = availability
            a.save()
        except Product.DoesNotExist:
            print(f'{code} not exist in db!!')
        except ProductAvailability.DoesNotExist:
            a = ProductAvailability(product_code=Product.objects.get(code=code),
                                    availability = availability)
            a.save()

