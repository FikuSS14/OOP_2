class OpenFiles:
    def __init__(self, file_name_list=None, encoding="utf-8"):
        self.file_name_list = file_name_list
        self.encoding = encoding
        self.file_data_list = []

    def open_files(self):
        for file in self.file_name_list:
            with open(file, "r", encoding=self.encoding) as f:
                data = f.read().split("\n")
                self.file_data_list.append(data)
        return self.file_data_list


class GetCookBook(OpenFiles):
    def __init__(self, file_name_list=None, our_product_list=None, encoding="utf-8"):
        super().__init__(file_name_list, encoding)
        self.our_product_list = our_product_list
        self.recipes_data_list = sum(self.open_files(), [])
        self.recipe_data_list = []
        self.cook_book = {}
        self.cook_book_choice = {}

    def get_boundary_indexes(self):
        gap_idx_list = []
        for idx in range(len(self.recipes_data_list)):
            if self.recipes_data_list[idx] == "":
                gap_idx_list.append(idx)
        return gap_idx_list

    def get_recipe_data_list(self):
        for idx1, idx2 in zip(
            [0] + self.get_boundary_indexes(),
            self.get_boundary_indexes() + [None],
            strict=False,
        ):
            if idx1 == 0:
                self.recipe_data_list.append(self.recipes_data_list[idx1:idx2])
            else:
                self.recipe_data_list.append(self.recipes_data_list[idx1 + 1 : idx2])
        return self.recipe_data_list

    def build_cook_book_dict(self):
        for recipe in self.get_recipe_data_list():
            food_name = recipe[0]
            ingridients_list = []
            ingridients_amount = int(recipe[1])
            for i in range(ingridients_amount):
                ingridient_data = recipe[2 + i].split(" | ")
                ingridients_list.append(
                    {
                        "ingredient_name": ingridient_data[0],
                        "quantity": int(ingridient_data[1]),
                        "measure": ingridient_data[2],
                    }
                )
            self.cook_book[food_name] = ingridients_list
        return self.cook_book

    def get_cook_book_dict(self):
        if self.our_product_list is None:
            self.our_product_list = list(self.build_cook_book_dict().keys())
            return self.build_cook_book_dict()
        else:
            if type(self.our_product_list) is list and len(self.our_product_list) > 0:
                for product in self.our_product_list:
                    if product in self.build_cook_book_dict():
                        self.cook_book_choice[product] = self.build_cook_book_dict()[
                            product
                        ]
        return self.cook_book_choice


class GetShopList(GetCookBook):
    def __init__(self, file_name_list=None, our_product_list=None):
        super().__init__(file_name_list, our_product_list)
        self.our_cook_book = self.get_cook_book_dict()
        self.ingridient_name_list = []
        self.ingridient_dict_list = []
        self.product_dict = {}

    def get_ingridients_list(self, dishes, person_count):
        if len(self.our_cook_book.keys()) > 0:
            if len(self.dishes) > 0:
                for dish in self.dishes:
                    if dish in self.our_cook_book:
                        ingridients = self.our_cook_book[dish]
                        for ingridient in ingridients:
                            self.ingridient_dict_list.append(ingridient)
                            self.ingridient_name_list.append(
                                ingridient["ingredient_name"]
                            )
        return self.ingridient_name_list, self.ingridient_dict_list

    def get_product_dict(
        self, dishes, person_count, ingridient_name_list, ingridient_dict_list
    ):
        for i in sorted(list(set(self.ingridient_name_list))):
            for my_dict in self.ingridient_dict_list:
                if my_dict["ingredient_name"] == i:
                    if i in self.product_dict:
                        self.product_dict[i]["quantity"] += (
                            my_dict["quantity"] * person_count
                        )
                    else:
                        self.product_dict[i] = {
                            "measure": my_dict["measure"],
                            "quantity": my_dict["quantity"] * person_count,
                        }
        return self.product_dict

    def get_shop_list(self, dishes=None, person_count=1):
        self.dishes = dishes
        self.dishes = [
            list(self.our_cook_book.keys()) if self.dishes is None else self.dishes
        ][0]
        self.person_count = person_count
        self.ingridient_name_list, self.ingridient_dict_list = (
            self.get_ingridients_list(
                dishes=self.dishes, person_count=self.person_count
            )
        )
        return self.get_product_dict(
            dishes=self.dishes,
            person_count=self.person_count,
            ingridient_name_list=self.ingridient_name_list,
            ingridient_dict_list=self.ingridient_dict_list,
        )


def get_shop_list_by_dishes(dishes=None, person_count=1):
    my_file_name_list = ["recipes.txt"]
    my_CookBook = GetCookBook(my_file_name_list, dishes)
    my_ShopList = GetShopList(my_CookBook.file_name_list, my_CookBook.our_product_list)
    if dishes is None:
        print(my_ShopList.get_shop_list(person_count=person_count))
    else:
        print(my_ShopList.get_shop_list(dishes, person_count))


class TextInfo(OpenFiles):
    def __init__(self, file_name_list=None, encoding="utf-8"):
        super().__init__(file_name_list, encoding)
        self.files_data = self.open_files()
        self.files_dict = {}
        self.files_dict_sorted = {}

    def get_files_dict(self):
        for idx, val in enumerate(self.file_name_list):
            self.files_dict[val] = {
                "len_text": len(self.files_data[idx]),
                "text": self.files_data[idx],
            }
        return self.files_dict

    def sort_dict(self):
        self.len_text_list = [
            self.get_files_dict()[k]["len_text"] for k in self.get_files_dict().keys()
        ]
        for l in sorted(list(set(self.len_text_list))):
            for f in self.file_name_list:
                if self.get_files_dict()[f]["len_text"] == l:
                    self.files_dict_sorted[f] = self.get_files_dict()[f]
                    for k in self.get_files_dict()[f]:
                        self.files_dict_sorted[f][k] = self.get_files_dict()[f][k]
        return self.files_dict_sorted

    def print_info(self):
        for k, v in self.sort_dict().items():
            print(k)
            for v2 in v.values():
                if type(v2) == int:
                    print(f"{v2}")
                else:
                    for s in v2:
                        print(s.strip())


print("***** ЗАДАНИЕ 1 *****")
print()
print("Словарь cook_book:")
print(GetCookBook(["recipes.txt"]).get_cook_book_dict())
print()
print("***** ЗАДАНИЕ 2 *****")
print()
print("Функция get_shop_list_by_dishes (заполнение списка блюд и количества персон):")
get_shop_list_by_dishes(["Запеченный картофель", "Омлет"], 6)
print()
print("***** ЗАДАНИЕ 3 *****")
print()
print("Выведение информации о содержимом в текстовых файлах:")
TextInfo(["1.txt", "2.txt", "3.txt"]).print_info()
