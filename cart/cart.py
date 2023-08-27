from django.conf import settings
from decimal import Decimal
from store.models import St


class Cart(object):

    def __init__(self, request):
        """
        Инициализируем корзину
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            #сохранить пустую корзину в сеансе
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, st, quantity=1, update_quantity=False):
        """
        Добавить продукт в корзину или обновить его количество.
        """
        St_id = str(st.id)
        if St_id not in self.cart:
            self.cart[St_id] = {'quantity': 0,
                'price': str(st.price)}
        if update_quantity:
            self.cart[St_id]['quantity'] = quantity
        else:
            self.cart[St_id]['quantity'] += quantity
        self.save()


    def save(self):
        self.session.modified = True

    def remove(self, st):
        """
        Удаление товара из корзины.
        """
        St_id = str(st.id)
        if St_id in self.cart:
            del self.cart[St_id]
            self.save()
        
    def __iter__(self):
        """
        Перебор элементов в корзине и получение продуктов из базы данных.
        """
        st_ids = self.cart.keys()
        # получение объектов st и добавление их в корзину
        games = St.objects.filter(id__in=st_ids)
        cart = self.cart.copy()
        for st in games:
            cart[str(st.id)]['st'] = st

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Подсчет всех товаров в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Подсчет стоимости товаров в корзине.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # удаление корзины из сессии
        del self.session[settings.CART_SESSION_ID]
        self.save()