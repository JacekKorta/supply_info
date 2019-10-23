from supply_info.models import ActiveProductList, PriceList, Product

"""
dane z pliku towary.txt
"""


def receive_main_data(data):
    for line in data.split('\n'):
        _, code, name, _, prod_group, _, _, _, price_a, _, price_b, _, price_c, _, price_d, _, _, _, mark, *_ \
            = line.split('\t')
        code = code[1:] if code.startswith(' ') else code
        name = name[1:] if name.startswith(' ') else name
        try:
            Product.objects.get(code=code)
            print(f'{code} already exist')
        except Product.DoesNotExist:
                prod = Product(code=code,
                               name=name,
                               prod_group=prod_group,
                               mark=mark)
                prod.save()
                p = PriceList(product_code=Product.objects.get(code=prod.code),
                              price_a=round(float(price_a), 2),
                              price_b=round(float(price_b), 2),
                              price_c=round(float(price_c), 2),
                              price_d=round(float(price_d), 2))
                p.save()
                a = ActiveProductList(product_code=Product.objects.get(code=prod.code))
                a.save()



