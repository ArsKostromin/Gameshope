from django.conf import settings
from decimal import Decimal
from store.models import St
from django.core.cache import cache


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
        #очистка кэша
        cache.delete('summa')
        cache.delete('summa1')

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
        cache.delete('summa')
        cache.delete('summa1')
        
    def __iter__(self):
        """
        Перебор элементов в корзине и получение продуктов из базы данных.
        """
        st_ids = self.cart.keys()
        # получение объектов st и добавление их в корзину
        st_ids = self.cart.keys()
        games = St.objects.filter(id__in=st_ids).select_related('genre')
        cart = self.cart.copy()
        for st in games:
            cart[str(st.id)]['st'] = st

        for item in cart.values():  # Изменено с self.cart на cart
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Подсчет всех товаров в корзине.
        """
        summa = cache.get('summa')
        if not summa:
            summa = sum(item['quantity'] for item in self.cart.values())
            cache.set('summa', summa, 60**3)
        return summa

    def get_total_price(self):
        """
        Подсчет стоимости товаров в корзине.
        """
        summa = cache.get('summa1')
        if not summa:
            summa = sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
            cache.set('summa1', summa, 60**3)
        return summa


    def clear(self):
        # удаление корзины из сессии
        del self.session[settings.CART_SESSION_ID]
        self.save()
        cache.delete('summa')
        cache.delete('summa1')