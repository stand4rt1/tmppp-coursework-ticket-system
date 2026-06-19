class CategoryComponent:
    def display(self, level: int = 0) -> None:
        raise NotImplementedError("Subclasses must implement this method.")


class CategoryLeaf(CategoryComponent):
    def __init__(self, name: str):
        # Leaf — конечная категория без вложенных элементов.
        self.name = name

    def display(self, level: int = 0) -> None:
        print("  " * level + f"- {self.name}")


class CategoryGroup(CategoryComponent):
    def __init__(self, name: str):
        # Composite — группа, которая может содержать другие группы и листья.
        self.name = name
        self.children: list[CategoryComponent] = []

    def add(self, component: CategoryComponent) -> None:
        self.children.append(component)

    def remove(self, component: CategoryComponent) -> None:
        self.children.remove(component)

    def display(self, level: int = 0) -> None:
        print("  " * level + f"+ {self.name}")

        for child in self.children:
            child.display(level + 1)


def build_default_category_tree() -> CategoryGroup:
    # Готовое дерево категорий для тикет-системы.
    support_department = CategoryGroup("Support Department")

    it_category = CategoryGroup("IT")
    hardware_category = CategoryGroup("Hardware")
    access_category = CategoryGroup("Access")

    hardware_category.add(CategoryLeaf("Printer Problems"))
    hardware_category.add(CategoryLeaf("Laptop Problems"))

    access_category.add(CategoryLeaf("Login Problems"))
    access_category.add(CategoryLeaf("Password Reset"))

    it_category.add(hardware_category)
    it_category.add(access_category)

    hr_category = CategoryGroup("HR")
    hr_category.add(CategoryLeaf("Documents"))
    hr_category.add(CategoryLeaf("Vacation Requests"))

    support_department.add(it_category)
    support_department.add(hr_category)

    return support_department