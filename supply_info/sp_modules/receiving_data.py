
from supply_info.models import ActiveProductList, PriceList, Product, ProductAvailability
from . import products_info

marks = {70: 'F',
         77: 'M'}


def receive_main_data(data):
    errors = []
    # dane z pliku 'towary.txt'
    for line in data.split('\n'):
        code, price_a, price_b, price_c, price_d, mark, name = line.split(';')
        manufacturer, type, sub_type, is_active = products_info.fill_category(code, mark)
        try:
            prod = Product.objects.get(code=code)
            p = PriceList.objects.get(product_code=prod)
            if [p.price_a, p.price_b, p.price_c, p.price_d] != [price_a, price_b, price_c, price_d]:
                p.save(update_fields=['price_a', 'price_b', 'price_c', 'price_d'])
                p.price_a = price_a
                p.price_b = price_b
                p.price_c = price_c
                p.price_d = price_d
                p.save(update_fields=['price_a', 'price_b', 'price_c', 'price_d'])
                print(f'{code} - prices was updated')
        except Product.DoesNotExist:
                prod = Product(code=code,
                               name=name[:400],
                               mark=marks.get(int(mark), ''),
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
                    a = ActiveProductList.objects.get(product_code=Product.objects.get(code=prod.code),
                                                      is_active=True)
                    a.save()
        except Exception as e:
            print(e)
            errors.append(f'{prod} - database error')
    print(errors)


def receive_availability_data(data):
    # dane z raportu: "bierzące stany i rezerwacje towarów"
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
                                    availability=availability)
            a.save()

