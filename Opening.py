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


print("***** ЗАДАНИЕ 1 *****")
print()
print("Словарь cook_book:")
print(GetCookBook(["recipes.txt"]).get_cook_book_dict())
