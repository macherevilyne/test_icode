import datetime

'''' Метод (конструктор) создания сущности Договор'''
class Contract:
    def __init__(self, name,project = None ):
        self.name = name #поле name задается при вызове класса, так как он в параметре
        self.date_create_contract =  datetime.datetime.now() # поле дата создания договора присваивается в момент вызова класса
        self.date_sign = None # по умолчанию дата подписания договора не установлена
        self.status = "Черновик" # статус по умолчанию
        self.project = project #поле project задается при вызове класса, так как он в параметре

# метод подтверждения договора, при вызове этого метода меняется статус договора и автоматически присваивается дата подписания
    # если есть атрибут project а по умолчанию нет (None), если есть то к проекту присваивается договор
    def confirm(self):
        if self.status == 'Черновик':
            self.status = 'Активен'
            self.date_sign = datetime.datetime.now()
            if self.project:
                self.project.add_contract(self)


# метод завершения договора
    def complete(self):
        if self.status == 'Активен':  # Изменяем статус только если договор активен
            self.status = 'Завершен'
            if self.project:
                self.project.complete_contract(self)

''''Метод (конструктор) создания сущности Проект'''
class Project:
    def __init__(self, name):
        self.name = name #поле name задается при вызове класса, так как он в параметре
        self.date_create_project = datetime.datetime.now() # поле дата создания проекта присваивается в момент вызова класс
        self.url_contract = [] # поле ссылка на договор


# Этот метод позволяет добавлять контракты к проекту, при условии, что контракты активны и их еще нет в списке контрактов проекта.
    def add_contract(self, contract):
        if contract.status == "Активен":
            if contract.project is None:
                self.url_contract.append(contract)
                contract.project = self

            else:
                print("Этот договор уже привязан к другому проекту.")
        else:
            print("Можно добавить только активный договор в проект.")

# Сначала перебираем ссылки на договора, если у контракта статус Активен вернуть True. По другому проверка на активность договора
    def has_active_contract(self):
        for contract in self.url_contract:
            if contract.status == "Активен":
                return True
        return False

# Метод удаления договора в проекте если он Активен
    def complete_contract(self, contract):
        if contract in self.url_contract and contract.status == 'Активен':
            contract.status = 'Завершен'


'''Создание основного меню приложения'''
class Menu():
    def __init__(self):
        self.url_contract = []
        self.projects = []


# метод для выбора дальнейших действий
    def choice(self):
        while True:
            print('Нажмите 1 если хотите работать с договорами')
            print('Нажмите 2 если хотите работать с проектами')
            print('Нажмите 3 чтобы активировать договор')
            print('Нажмите 4 чтобы присвоить проекту договор')
            print('Нажмите 5 если хотите посмотреть список договоров и проектов')
            print('Нажмите 6 если хотите завершить договор')
            print('Нажмите 7 если хотите завершить работу с программой')

            choice = input("Выберите действие: ")
            if choice == '1':
                self.create_contract()


            elif choice == '2':
                if any(contract.status == 'Активен' for contract in self.url_contract):
                    self.create_project()
                else:
                    print("Нельзя создать проект. Нет активных договоров.")

            elif choice == '3':
                self.confirm_contract()

            elif choice == '4':
                self.add_contract_to_project()

            elif choice == '5':
                self.list_()

            elif choice == '6':
                self.complete_contract()
            elif choice == '7':
                print('Работа с программой завершена')
                break


# Метод создания нового договора

    def create_contract(self):
        name = input('Введите название контракта:'
                     )
        contract = Contract(name)
        self.url_contract.append(contract)
        print(f'Создан договор {name}')

# Метод создания нового проекта
    def create_project(self):
        name = input('Введите название проекта: '
                     )
        project = Project(name)
        self.projects.append(project)
        print(f'Создан проект {name}')
# Метод получения списка всех договоров и проектов, а так же статус договора
    def list_(self):
        contract_details = [f'{contract.name} ({contract.status})' for contract in self.url_contract]
        project_names = [project.name for project in self.projects]
        print(f'Список актуальных проектов: {project_names} и договоров: {contract_details}')

# Метод активация договора
    def confirm_contract(self):

        print("Список доступных договоров:")
        for i, contract in enumerate(self.url_contract, 1):
            print(f"{i}. {contract.name}")

        contract_choice = input("Выберите номер договора для подтверждения: ")
        try:
            contract_choice = int(contract_choice)
            if 1 <= contract_choice <= len(self.url_contract):
                contract = self.url_contract[contract_choice - 1]
                if contract.status == 'Черновик':
                    contract.status = 'Активен'
                    print(f"Договор '{contract.name}' успешно подтвержден.")
                else:
                    print("Можно подтвердить только договор со статусом 'Черновик'.")
            else:
                print("Некорректный выбор договора.")
        except ValueError:
            print("Введите корректный номер договора.")

# Метод добавления в проект активный договор
    def add_contract_to_project(self):

        print("Список доступных проектов:")
        for i, project in enumerate(self.projects, 1):
            print(f"{i}. {project.name}")

        project_choice = input("Выберите номер проекта для добавления договора: ")
        try:
            project_choice = int(project_choice)
            if 1 <= project_choice <= len(self.projects):
                project = self.projects[project_choice - 1]

                print("Список доступных договоров:")
                for i, contract in enumerate(self.url_contract, 1):
                    print(f"{i}. {contract.name}")

                contract_choice = input("Выберите номер договора для добавления к проекту: ")
                try:
                    contract_choice = int(contract_choice)
                    if 1 <= contract_choice <= len(self.url_contract):
                        contract = self.url_contract[contract_choice - 1]
                        if contract.status == 'Активен':
                            project.add_contract(contract)
                            print(f"Договор '{contract.name}' успешно добавлен к проекту '{project.name}'.")
                        else:
                            print("Можно добавить только активный договор в проект.")
                    else:
                        print("Некорректный выбор договора.")
                except ValueError:
                    print("Введите корректный номер договора.")
            else:
                print("Некорректный выбор проекта.")
        except ValueError:
            print("Введите корректный номер проекта.")

# Метож завершения активного договора у проекта

    def complete_contract(self):
        print("Список доступных проектов:")
        for i, project in enumerate(self.projects, 1):
            print(f"{i}. {project.name}")

        project_choice = input("Выберите номер проекта: ")
        try:
            project_choice = int(project_choice)
            if 1 <= project_choice <= len(self.projects):
                project = self.projects[project_choice - 1]

                if not project.has_active_contract():
                    print("Нет активных договоров для завершения в данном проекте.")
                    return

                print("Список доступных договоров в проекте:")
                for i, contract in enumerate(project.url_contract, 1):
                    print(f"{i}. {contract.name}")

                contract_choice = input("Выберите номер договора для завершения: ")
                try:
                    contract_choice = int(contract_choice)
                    if 1 <= contract_choice <= len(project.url_contract):
                        contract = project.url_contract[contract_choice - 1]

                        if contract.status == 'Активен':
                            contract.status = 'Завершен'
                            print(f"Договор '{contract.name}' успешно завершен.")
                        else:
                            print("Можно завершить только договор со статусом 'Активен'.")
                    else:
                        print("Некорректный выбор договора.")
                except ValueError:
                    print("Введите корректный номер договора.")
            else:
                print("Некорректный выбор проекта.")
        except ValueError:
            print("Введите корректный номер проекта.")

# Создания и вызов объекта и метода
main_menu = Menu()
main_menu.choice()
