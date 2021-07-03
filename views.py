import os.path as OP
import datetime as DT


class ViewsPages:
    def __init__(self):
        self.cr = None
        self.general_template = 'templates/HTML/general_template2.html'

        # Словарь шаблонов страницы матрицы Эйзенхауэра
        self.MatrixEisenhowerDictionary2 = {
            'title': ('text', ('MatrixEisenhower',)),
            'css': ('file', ('templates/CSS/main.css', 'templates/CSS/task.css')),
            'header': ('text', ('<h1>Матрица Эйзенхауэра</h1>',
                                '<a class="header_link" href="/Projects">Проекты</a>',
                                '<a class="header_link" href="/Tasks">Задачи</a>')),
            'main': ('file', ('templates/HTML/matrix_eisenhower.html',)),
            'right': ('file', ('templates/HTML/block_right.html',)),
            'tasks': ('file', ('templates/HTML/task_card.html',)),
            'list_plan_works1': ('file', ('templates/HTML/plan_work_card.html',)),
            'list_plan_works2': ('file', ('templates/HTML/plan_work_card.html',)),
            'list_plan_works3': ('file', ('templates/HTML/plan_work_card.html',)),
            'list_plan_works4': ('file', ('templates/HTML/plan_work_card.html',)),
            'header_tasks': ('file', ('templates/HTML/header_tasks.html',)),
            'header_time_stamps': ('file', ('templates/HTML/header_time_stamps.html',)),
            'time_stamps': ('file', ('templates/HTML/time_stamp_card.html',)),
            'mini_form': ('file', ('templates/HTML/time_stamp_form.html', 'templates/HTML/plan_work_form.html')),
            'task_form_main': ('file', ('templates/HTML/task_form.html',)),
            'script': ('file', ('templates/JS/main.js',))
        }

        # Словарь шаблонов страницы задач
        self.TasksPageDictionary2 = {
            'title': ('text', ('Tasks',)),
            'css': ('file', ('templates/CSS/main.css', 'templates/CSS/task.css')),
            'header': ('text', ('<h1>Задачи</h1>',
                                '<a class="header_link" href="/">Матрица Эйзенхауэра</a>',
                                '<a class="header_link" href="/Projects">Проекты</a>')),
            'main': ('file', ('templates/HTML/task_area.html',)),
            'right': ('file', ('templates/HTML/block_right.html',)),
            'tasks': ('file', ('templates/HTML/task_card.html',)),
            'mini_form': ('file', ('templates/HTML/time_stamp_form.html', 'templates/HTML/plan_work_form.html')),
            'script': ('file', ('templates/JS/main.js',)),
            'block_time_stamps': ('file', ('templates/HTML/block_time_stamps.html',)),
            'header_time_stamps': ('file', ('templates/HTML/header_time_stamps.html',)),
            'header_tasks': ('file', ('templates/HTML/header_tasks.html',)),
            'time_stamps': ('file', ('templates/HTML/time_stamp_card.html',)),
            'task_form_main': ('file', ('templates/HTML/task_form.html',))
        }

        # Словарь шаблонов страницы проектов
        self.ProjectPageDictionary2 = {
            'title': ('text', ('Projects',)),
            'css': ('file', ('templates/CSS/main.css', 'templates/CSS/task.css')),
            'header': ('text', ('<h1>Проекты</h1>',
                                '<a class="header_link" href="/">Матрица Эйзенхауэра</a>',
                                '<a class="header_link" href="/Tasks">Задачи</a>')),
            'script': ('file', ('templates/JS/main.js',)),
            'right': ('file', ('templates/HTML/block_right.html',)),
            'tasks': ('file', ('templates/HTML/task_card.html',)),
            'mini_form': ('file', ('templates/HTML/time_stamp_form.html', 'templates/HTML/plan_work_form.html')),
            'main': ('file', ('templates/HTML/block_projects.html',)),
            'project_form_main': ('file', ('templates/HTML/project_form.html',)),
            'header_list_projects': ('file', ('templates/HTML/header_list_projects.html',)),
            'block_time_stamps': ('file', ('templates/HTML/block_time_stamps.html',)),
            'header_time_stamps': ('file', ('templates/HTML/header_time_stamps.html',)),
            'header_tasks': ('file', ('templates/HTML/header_tasks.html',)),
            'time_stamps': ('file', ('templates/HTML/time_stamp_card.html',)),
            'list_projects': ('file', ('templates/HTML/project_card.html',))
        }

        # Словарь ссылок к иконкам
        self.image_links = {
            'main_img': 'https://cdn.fishki.net/upload/post/201503/23/1474732/2_16.jpg',
            'delete_img': 'https://cdn2.iconfinder.com/data/icons/round-interface-1/217/50-512.png',
            'save_img': 'https://nskphone.ru/upload/medialibrary/d48/d48e3323eeaa7e4def207778d5d86bdd.png',
            'close_img': 'https://www.pngkey.com/png/full/19-190511_red-cross-x-clip-art-error-icon-transparent.png',
            'mark_time_img': 'https://spb.ramsaydiagnostics.ru/images/prices_banners/stock_alarm_svg.png',
            'planned_time_img': 'https://opt-stroymarket.ru/files/image/%D0%9D%D0%BE%D0%B2%D0%B0%D1%8F%D0%9F%D0%B0%'
                                'D0%BF%D0%BA%D0%B0/Scheduling-Icon.png',
            'list_time_stamp_img': 'https://cdn4.iconfinder.com/data/icons/ios7-active-2/512/Management.png',
            'on_execution_img': 'https://www.vippng.com/png/full/224-2243484_automation-icon-png-click2cloud-'
                                'disease-control-icon.png',
            'new_img': 'https://cdn3.iconfinder.com/data/icons/ikooni-flat-online-shopping/128/shopping-16-512.png',
            'cancelled_img': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Simple_Prohibited.svg/1200px-'
                             'Simple_Prohibited.svg.png',
            'executed': 'https://al-teh.ru/wa-data/public/shop/img/reshenie-green.png',
            'add_object_img': 'https://cdn.pixabay.com/photo/2014/03/25/17/00/plus-297823_1280.png'
        }

    # ****************МЕТОДЫ ГЕНЕРАЦИИ КОДА СТРАНИЦЫ ИЗ ФАЙЛОВ ШАБЛОНОВ*****************
    @staticmethod
    def get_code_from_file(path_file):
        """ Получаем список строк кода из файла """
        insert_cod = list()
        if OP.exists(path_file):
            with open(path_file, 'r', encoding="utf8") as template:
                list_string = template.readlines()
                for code_string in list_string:
                    insert_cod.append(code_string)
        else:
            print(f'Файла по пути "{path_file}" не существует!')
        return insert_cod

    def fill_field_form(self, path, fields, indent):
        """ Заполняем поля карточек и форм данными
         path: путь к файлу с html кодом формы;
         fields: список значений для заполняемых полей, поля заполняются по очереди,
         заменяя ключевое слово вставки '{%||%}' значениями из списка
         indent: отступ перед вставляемым кодом"""
        # Извлекаемый код
        result_cod = ''
        list_fields = fields
        # Дробим файл на строки
        list_string_cod = self.get_code_from_file(path)
        for cod_string in list_string_cod:
            if cod_string.find('{%||%}') != -1:
                new_str = self.replace_keyword_with_value(cod_string, list_fields)
                result_cod += self.get_processed_string(new_str, indent)
            else:
                result_cod += self.get_processed_string(cod_string, indent)

        return result_cod

    def replace_keyword_with_value(self, string_cod, fields):
        """ Заменяем во входящей строке string_cod конструкции замены '{%||%}'
        на значение полей из списка fields """
        processed_string = string_cod
        if processed_string.find('{%||%}') != -1 and fields:
            processed_string = processed_string.replace("{%||%}", str(fields[0]), 1)
            fields.pop(0)
            return self.replace_keyword_with_value(processed_string, fields)
        else:
            return processed_string

    def get_code_list(self, path_file, name_list, indent):
        """ Метод для выбора метода генерации кода списка в зависимости от имени блока """
        # Реестр задач на провей панели
        if name_list == 'tasks':
            return self.get_list_task_code(path_file, indent)
        # Реестры плановых работ в матрице на главной панели
        elif name_list == 'list_plan_works1':
            return self.get_list_plan_work_code(path_file, indent, 1)
        elif name_list == 'list_plan_works2':
            return self.get_list_plan_work_code(path_file, indent, 2)
        elif name_list == 'list_plan_works3':
            return self.get_list_plan_work_code(path_file, indent, 3)
        elif name_list == 'list_plan_works4':
            return self.get_list_plan_work_code(path_file, indent, 4)
        # Реестр проектов
        elif name_list == 'list_projects':
            return self.get_list_projects_code(path_file, indent)
        elif name_list == 'time_stamps':
            return self.get_list_task_time_stamps(
                path_file, indent, self.cr.global_parameters.get('type_filter_time_stamps_list'),
                self.cr.global_parameters.get('id_object'))
        else:
            print('*****************Нет такого блока**************************')

    def get_code_form(self, path_file, name_form, indent):
        """ Метод для выбора метода генерации кода формы в зависимости от имени формы """
        if name_form == 'mini_form':
            return self.get_plan_work_form_cod(path_file, indent)
        elif name_form == 'task_form_main':
            return self.get_task_cod_form(path_file, indent, self.cr.global_parameters.get('id_task'))
        elif name_form == 'header_time_stamps':
            return self.get_header_time_stamp_list_cod(path_file)
        elif name_form == 'header_tasks':
            return self.get_header_tasks_list_cod(path_file, indent)
        elif name_form == 'header_list_projects':
            return self.get_header_projects_list_cod(path_file, indent)
        else:
            print('*****************Нет такого блока**************************')

    @staticmethod
    def get_processed_string(string_cod, indent=0):
        """ Дорабатываем строки в реестре с учетом отступов и перевода строки """
        new_string = string_cod
        if new_string.find('\n') == -1:
            new_string = ' ' * indent + new_string + '\n'
        else:
            new_string = ' ' * indent + new_string

        return new_string

    def check_for_files(self, files):
        """ Проверяем передаваемые для вставки файлы на наличие по указанным путям
        Извлекаем массив не найденных заявленных файлов """
        not_file = list()
        if not OP.exists(self.general_template):
            not_file.append(self.general_template)

        for file_tuple in files:
            if file_tuple[0] == 'file':
                for file in file_tuple[1]:
                    if not OP.exists(file):
                        not_file.append(file)
        return not_file

    def generate_page_code_recursion(self, path_file, indent, files):
        """ Генератор кода страницы, принимает на вход:
        path_file: путь к файлу, с которого начинается генерация (тип вставки только block);
        indent: отступ от от левого края; files: словарь с ключами ==
        наменованию блоков для вставки, и значениям в виде кортежа,
        где первый элемент - вид данных: file - данные надо считать из файла,
        text - код предоставлен в виде списка строк;
        второй элемент - данные: путь к файлу, если file или
        список строк, если text
        Извлекает код всей таблицы если path_file - путь к шаблону, или код одного из блоков,
        если path_file - путь к одному из вложенных блоков """

        # Проверяем наличие всех заявленных файлов в списке, если чего-то не хватает - кидаем заглушку
        check_for_files = self.check_for_files(files)
        if check_for_files:
            return f'''<h1>NOT FOUND FILE</h1><br><p>Не найдено файлов: {str(check_for_files).strip('[]')}</p>'''

        # Извлекаемый код страницы
        result_cod = ''

        # Обрабатываем строки
        # Если это html файл, то ищем ключевые слова
        if path_file.split('.')[1] == 'html':
            # Дробим построчно файл, с которого начинается генерация, проверяем каждую строку на наличие блоков вставки
            for str_file in self.get_code_from_file(path_file):
                if str_file.find('%|||%') != -1:
                    sub_str = str_file.split()
                    if sub_str[0] == '%|||%' and sub_str[len(sub_str) - 1] == '%|||%' and \
                            sub_str[1] in ('block', 'list', 'form') and sub_str[2] in files:
                        # Дополнительный отступ при генерации списка строк
                        add_indent = str_file.find('%')
                        if files[sub_str[2]][0] == 'file':
                            # Вставляем код из файлов по ключу из словаря files
                            for file in files[sub_str[2]][1]:
                                add_cod = ''
                                # Если тип контента 'block' то запускаем рекурсию
                                if sub_str[1] == 'block' and sub_str[2] in files:
                                    add_cod = self.generate_page_code_recursion(file, indent + add_indent, files)
                                # Если тип контента 'list' то запускаем списочный метод
                                elif sub_str[1] == 'list' and sub_str[2] in files:
                                    add_cod = self.get_code_list(file, sub_str[2], indent + add_indent)
                                # Если тип контента 'form' то запускаем метод заполения полей формы
                                elif sub_str[1] == 'form' and sub_str[2] in files:
                                    add_cod = self.get_code_form(file, sub_str[2], indent + add_indent)
                                if add_cod:
                                    result_cod += add_cod

                        else:
                            # Если тип вставляемых данных текст - то вставляем с обработкой
                            for code_string in files[sub_str[2]][1]:
                                result_cod += self.get_processed_string(code_string, indent)
                    # Если конструкция вставки содержит не описанный в словаре files блок, то вставляем как есть
                    else:
                        result_cod += str_file
                # Если строка не содержит символов вставки, вставляем как есть
                else:
                    result_cod += str_file
        # Если это css или js файлы, то просто дробим файл на строки и добавляем в код страницы
        else:
            for code_string in self.get_code_from_file(path_file):
                result_cod += self.get_processed_string(code_string, indent)

        return result_cod

    # ****************МЕТОДЫ ОТРИСОВКИ ПРОЕКТОВ*****************
    def get_list_projects_code(self, path_file, indent):
        """ Генерирует код списка проектов для окна main на страницах """
        result_cod = ''
        # Получаем список словарей с полями задач
        list_dict = self.cr.get_list_projects()

        if list_dict:
            result_cod += '\n<div id="insert_project">\n</div>'
            for fields in list_dict:
                # Данные по задаче из словаря выставляем в список в порядке их вставки в шаблон карточки
                title, icon, date_end = '', '', ''
                if fields.get('status_project') == 1:
                    title = 'Проект в работе'
                    icon = self.image_links.get('on_execution_img')
                    date_end = fields.get('date_end_plan')
                elif fields.get('status_project') == 2:
                    title = 'Проект завершен'
                    icon = self.image_links.get('executed')
                    date_end = fields.get('date_end_fact')
                elif fields.get('status_project') == 3:
                    title = 'Проект отменен'
                    icon = self.image_links.get('cancelled_img')
                    date_end = fields.get('date_end_plan')

                price = round((fields.get('time_fact')/8)*2500, 2)
                day_fact = round((fields.get('time_fact')/8), 2)
                day_plan = round((fields.get('time_plan') / 8), 2)
                list_field = [
                    fields['id'], fields['id'], title, icon,
                    DT.date.strftime(DT.datetime.strptime(fields['date_begin'], '%Y-%m-%d').date(), '%d.%m.%Y') if
                    fields['date_begin'] != '' else fields['date_begin'],
                    fields['id'], fields['name_project'],
                    DT.date.strftime(DT.datetime.strptime(date_end, '%Y-%m-%d').date(), '%d.%m.%Y') if
                    date_end != '' else date_end,
                    '', fields['time_fact'], fields['time_plan'], day_fact, day_plan, price
                ]

                # Заполняем поля карточек и форм данными
                result_cod += self.fill_field_form(path_file, list_field, indent)
            return result_cod
        else:
            return self.get_processed_string('<h3>Проектов нет</h3>', indent)

    def get_project_form_cod(self, path_file, indent, id_project=0):
        """ Генерируем код формы проекта """
        result_cod = ''

        id_project = int(id_project)

        if id_project == 0:
            # Получаем код формы нового проекта
            list_field = [
                'Новый проект', self.image_links.get('new_img'), '-', self.image_links.get('close_img'),
                '', self.image_links.get('save_img'),
                'closeProject()', self.image_links.get('delete_img'),
                '', '', '', 1, '', '', '', 0,
                '', self.image_links.get('list_time_stamp_img'),
                '', self.image_links.get('cancelled_img'),
                '', self.image_links.get('executed'),
                0
            ]
            result_cod += self.fill_field_form(path_file, list_field, indent)
        else:
            # Получаем код формы сохраненного проекта
            project_dict = self.cr.get_list_projects(id_project)
            if project_dict and type(project_dict) == list and len(project_dict) == 1:
                project_dict = project_dict[0]

                title_status = ''
                paint_status = ''
                if project_dict.get('status_project') == 0:
                    paint_status = self.image_links.get('new_img')
                    title_status = 'Новая задача'
                elif project_dict.get('status_project') == 1:
                    paint_status = self.image_links.get('on_execution_img')
                    title_status = 'Задача в работе'
                elif project_dict.get('status_project') == 2:
                    title_status = 'Задача выполнена'
                    paint_status = self.image_links.get('executed')
                elif project_dict.get('status_project') == 3:
                    paint_status = self.image_links.get('cancelled_img')
                    title_status = 'Задача отменена'
                list_field = [
                    title_status, paint_status, str(id_project), self.image_links.get('close_img'),
                    id_project, self.image_links.get('save_img'),
                    'deleteProject(' + str(id_project) + ')', self.image_links.get('delete_img'),
                    project_dict.get('name_project'), project_dict.get('date_begin'),
                    project_dict.get('date_end_plan'), project_dict.get('time_plan'),
                    project_dict.get('content_project'), project_dict.get('execution_comment'),
                    project_dict.get('date_end_fact'), project_dict.get('time_fact'),
                    "drawListTimeStamp('project', " + str(id_project) + ")",
                    self.image_links.get('list_time_stamp_img'),
                    str(id_project) + ', 3', self.image_links.get('cancelled_img'),
                    str(id_project) + ', 2', self.image_links.get('executed'),
                    project_dict.get('status_project')
                ]
                result_cod += self.fill_field_form(path_file, list_field, indent)

        return result_cod

    def get_header_projects_list_cod(self, path_file, indent=4):
        """ Изввлекает код заголовка для реестра проектов """
        result_cod = ''
        list_field = list()

        list_field.append(self.get_code_filter_status_project())
        list_field.append(self.image_links.get('add_object_img'))

        # Заполняем поля карточек и форм данными
        result_cod += self.fill_field_form(path_file, list_field, indent)

        return result_cod

    # ****************МЕТОДЫ ОТРИСОВКИ ЗАДАЧ*****************
    def get_list_task_code(self, path_file, indent, id_task=0):
        """ Генерирует код списка задач для окна right на страницах """
        result_cod = ''

        # Получаем список словарей с полями задач
        list_dict = self.cr.get_list_task(id_task)

        if list_dict:
            result_cod += '\n<div id="insert_task">\n</div>'
            for fields in list_dict:
                class_card = 'task_card'
                if fields['type_task'] == 1:
                    class_card = 'task_card ' + 'urgent-important'
                elif fields['type_task'] == 3:
                    class_card = 'task_card ' + 'urgent-unimportant'
                elif fields['type_task'] == 2:
                    class_card = 'task_card ' + 'non-urgent-important'
                elif fields['type_task'] == 4:
                    class_card = 'task_card ' + 'non-urgent-unimportant'

                title_status = ''
                paint_status = ''
                if fields.get('status_stage') == 0:
                    paint_status = self.image_links.get('new_img')
                    title_status = 'Новая задача'
                elif fields.get('status_stage') == 1:
                    paint_status = self.image_links.get('on_execution_img')
                    title_status = 'Задача в работе'
                elif fields.get('status_stage') == 2:
                    title_status = 'Задача выполнена'
                    paint_status = self.image_links.get('executed')
                elif fields.get('status_stage') == 3:
                    paint_status = self.image_links.get('cancelled_img')
                    title_status = 'Задача отменена'

                # Данные по задаче из словаря выставляем в список в порядке их вставки в шаблон карточки
                list_field = [
                    fields['id'], class_card, fields['id'], title_status, paint_status,
                    fields['name_project'], fields['name_stage'],
                    DT.date.strftime(DT.datetime.strptime(fields['date_begin'], '%Y-%m-%d').date(), '%d.%m.%Y') if
                    fields['date_begin'] != '' else fields['date_begin'],
                    DT.date.strftime(DT.datetime.strptime(fields['date_end_plan'], '%Y-%m-%d').date(), '%d.%m.%Y') if
                    fields['date_end_plan'] != '' else fields['date_end_plan'],
                    fields['time_fact'], fields['time_plan'],
                    fields['id'], fields['content_task'],
                    fields.get('id'), self.image_links.get('mark_time_img'),
                    fields.get('id'), self.image_links.get('list_time_stamp_img'),
                    fields.get('id'), self.image_links.get('planned_time_img'),
                ]

                # Заполняем поля карточек и форм данными
                result_cod += self.fill_field_form(path_file, list_field, indent)
            return result_cod
        else:
            return self.get_processed_string('<h3>Задач нет</h3>', indent)

    def get_update_list_task_code(self, id_task):
        """ Генерирует код для измененной задачи для окна right на страницах """
        result_cod = self.get_list_task_code(self.TasksPageDictionary2.get('tasks')[1][0], 8, id_task)
        # Удаляем первую и последнюю строку, т.к. они уже есть на странице
        list_str = result_cod.split('\n')
        list_str.pop(0)
        list_str.pop(0)
        list_str.pop(0)
        list_str.pop(len(list_str) - 1)
        list_str.pop(len(list_str) - 1)
        result_cod = ''
        for one_string in list_str:
            result_cod += one_string + '\n'
        print(result_cod)

        return result_cod

    def get_header_tasks_list_cod(self, path_file, indent=4):
        """ Изввлекает код заголовка для реестра задач в правой панели """
        result_cod = ''
        list_field = list()

        list_field.append(self.get_code_filter_status_task())
        list_field.append(self.get_code_filter_select_project())

        # Заполняем поля карточек и форм данными
        result_cod += self.fill_field_form(path_file, list_field, indent)

        return result_cod

    def get_task_cod_form(self, path_file, indent, id_task=0):
        """ Генерируем код формы задачи """
        result_cod = ''
        class_areas = ''
        today = DT.date.today()
        if id_task == 0:
            class_areas = 'block_field area_wish_color1'
            task_dict = {'id': 0, 'content_task': '', 'type_task': 1,
                         'date_begin': today, 'date_end_plan': today, 'date_end_fact': '',
                         'time_plan': 1, 'time_fact': 0, 'execution_comment': '',
                         'id_project': 0, 'id_stage_project': 0, 'status_stage': 0,
                         'name_project': '-', 'name_stage': '-'
                         }
        else:
            task_dict = self.cr.get_list_task(id_task)[0]
            print(task_dict)
            if task_dict.get('type_task') == 1:
                class_areas = 'block_field area_wish_color1'
            elif task_dict.get('type_task') == 2:
                class_areas = 'block_field area_wish_color2'
            elif task_dict.get('type_task') == 3:
                class_areas = 'block_field area_wish_color3'
            elif task_dict.get('type_task') == 4:
                class_areas = 'block_field area_wish_color4'

        title_status = ''
        paint_status = ''
        if task_dict.get('status_stage') == 0:
            paint_status = self.image_links.get('new_img')
            title_status = 'Новая задача'
        elif task_dict.get('status_stage') == 1:
            paint_status = self.image_links.get('on_execution_img')
            title_status = 'Задача в работе'
        elif task_dict.get('status_stage') == 2:
            title_status = 'Задача выполнена'
            paint_status = self.image_links.get('executed')
        elif task_dict.get('status_stage') == 3:
            paint_status = self.image_links.get('cancelled_img')
            title_status = 'Задача отменена'

        insert_types = self.get_code_select_types(task_dict.get('type_task'))
        insert_projects = self.get_code_select_project(task_dict.get('id_project'))
        insert_stage = ''
        number_task = task_dict.get('id') if task_dict.get('status_stage') != 0 else '_'

        list_field = [
            class_areas, title_status, paint_status, number_task, self.image_links.get('close_img'),
            task_dict.get('id'), self.image_links.get('save_img'),
            task_dict.get('id'), self.image_links.get('delete_img'),
            class_areas, insert_types, insert_projects, insert_stage,
            class_areas, task_dict.get('date_begin'), task_dict.get('date_end_plan'), task_dict.get('time_plan'),
            class_areas, task_dict.get('content_task'),
            class_areas, task_dict.get('execution_comment'),
            class_areas, task_dict.get('date_end_fact'), task_dict.get('time_fact'),
            task_dict.get('id'), self.image_links.get('mark_time_img'),
            task_dict.get('id'), self.image_links.get('list_time_stamp_img'),
            task_dict.get('id'), self.image_links.get('planned_time_img'),
            task_dict.get('id'), self.image_links.get('cancelled_img'),
            task_dict.get('id'), self.image_links.get('executed'),
            task_dict.get('status_stage'), task_dict.get('id')
        ]
        # Заполняем поля карточек и форм данными
        result_cod += self.fill_field_form(path_file, list_field, indent)

        return result_cod

    # ****************МЕТОДЫ ОТРИСОВКИ ПЛАНОВЫХ РАБОТ*****************
    def get_list_plan_work_code(self, path_file, indent, type_task, id_plan_work=0):
        """ Генерирует код списка плановых работ для квадратов матрицы
         основной панели на странице матрицы эйзенхауэра """
        result_cod = ''

        # Получаем список словарей с полями задач
        list_dict = list()
        if type_task != 0:
            list_dict = self.cr.get_list_plan_works(type_task)
        elif id_plan_work != 0:
            list_dict = self.cr.get_list_plan_works(0, id_plan_work)

        if list_dict:
            tyt = str(list_dict[0]['type_task'])
            result_cod += f'\n<div id="insert_plan_work{tyt}">\n</div>'
            for fields in list_dict:
                class_card = 'plan_work_card'

                print(fields)

                # Данные по задаче из словаря выставляем в список в порядке их вставки в шаблон карточки
                list_field = [
                    fields['id'], class_card, fields['id'], self.image_links.get('planned_time_img'),
                    fields['name_project'], fields['name_stage'],
                    fields['time_plan_work'],
                    DT.date.strftime(DT.datetime.strptime(fields['date_begin'], '%Y-%m-%d').date(), '%d.%m.%Y') if
                    fields['date_begin'] != '' else fields['date_begin'],
                    DT.date.strftime(DT.datetime.strptime(fields['date_end_plan'], '%Y-%m-%d').date(), '%d.%m.%Y') if
                    fields['date_end_plan'] != '' else fields['date_end_plan'],
                    fields['time_fact'], fields['time_plan'],
                    fields['id_task'], fields['content_task'],
                    fields['id'], fields['planned_work'],
                    fields.get('id'), self.image_links.get('cancelled_img'),
                    str(fields.get('id_task')) + ', ' + str(fields.get('id')), self.image_links.get('executed'),
                    fields.get('id_task'), self.image_links.get('mark_time_img')
                ]

                # Заполняем поля карточек и форм данными
                result_cod += self.fill_field_form(path_file, list_field, indent)
            return result_cod
        else:
            return self.get_processed_string('<h3>Запланированных работ нет</h3>', indent)

    def get_update_list_plan_work_code(self, id_plan_work):
        """ Генерирует код измененной плановой работы для квадратов матрицы
         основной панели на странице матрицы эйзенхауэра """
        result_cod = ''

        # Получаем список словарей с полями задач
        list_dict = self.cr.get_list_plan_works(0, id_plan_work)
        if list_dict:
            for fields in list_dict:
                class_card = 'plan_work_card'

                print(fields)

                # Данные по плановой работе из словаря выставляем в список в порядке их вставки в шаблон карточки
                list_field = [
                    fields['id'], class_card, fields['id'], self.image_links.get('planned_time_img'),
                    fields['name_project'], fields['name_stage'],
                    fields['time_plan_work'],
                    DT.date.strftime(DT.datetime.strptime(fields['date_begin'], '%Y-%m-%d').date(), '%d.%m.%Y') if
                    fields['date_begin'] != '' else fields['date_begin'],
                    DT.date.strftime(DT.datetime.strptime(fields['date_end_plan'], '%Y-%m-%d').date(), '%d.%m.%Y') if
                    fields['date_end_plan'] != '' else fields['date_end_plan'],
                    fields['time_fact'], fields['time_plan'],
                    fields['id_task'], fields['content_task'],
                    fields['id'], fields['planned_work'],
                    fields.get('id'), self.image_links.get('cancelled_img'),
                    str(fields.get('id_task')) + ', ' + str(fields.get('id')), self.image_links.get('executed'),
                    fields.get('id_task'), self.image_links.get('mark_time_img')
                ]

                # Заполняем поля карточек и форм данными
                result_cod += self.fill_field_form(self.MatrixEisenhowerDictionary2.get('list_plan_works1')[1][0],
                                                   list_field, 8)
                # Удаляем первую и последнюю строку, т.к. они уже есть на странице
                list_str = result_cod.split('\n')
                list_str.pop(0)
                list_str.pop(len(list_str) - 1)
                result_cod = ''
                for one_string in list_str:
                    result_cod += one_string + '\n'

        return result_cod

    def get_plan_work_form_cod(self, path_file, id_object, status=0):
        """ Генерируем код формы плановой работы """
        result_cod = ''

        # Генерация кода новой плановой работы
        if status == 0:
            # Получаем словарь с полями задачи, к которой привязана плановая работа
            list_dict = self.cr.get_list_task(id_object)

            if list_dict:
                for fields in list_dict:
                    class_form = 'block_mini_form'
                    if fields['type_task'] == 1:
                        class_form = 'block_mini_form ' + 'urgent-important'
                    elif fields['type_task'] == 3:
                        class_form = 'block_mini_form ' + 'urgent-unimportant'
                    elif fields['type_task'] == 2:
                        class_form = 'block_mini_form ' + 'non-urgent-important'
                    elif fields['type_task'] == 4:
                        class_form = 'block_mini_form ' + 'non-urgent-unimportant'

                    # today_date = self.cr.db.todayDate()

                    # Данные по задаче из словаря выставляем в список в порядке их вставки в шаблон карточки
                    list_field = [class_form, 'Новая плановая работа', self.image_links.get('new_img'),
                                  self.image_links.get('close_img'),
                                  'saveNewPlanWorkForm(' + str(fields['id']) + ', ' + str(fields['type_task']) + ')',
                                  self.image_links.get('save_img'),
                                  'close_mini_form()', self.image_links.get('delete_img'),
                                  '_', fields['name_project'], fields['name_stage'],
                                  DT.date.strftime(DT.datetime.strptime(fields['date_begin'], '%Y-%m-%d').date(),
                                                   '%d.%m.%Y') if fields['date_begin'] != '' else
                                  fields['date_begin'],
                                  DT.date.strftime(DT.datetime.strptime(fields['date_end_plan'], '%Y-%m-%d').date(),
                                                   '%d.%m.%Y') if fields['date_end_plan'] != '' else
                                  fields['date_end_plan'],
                                  fields['time_fact'], fields['time_plan'],
                                  fields['id'], fields['content_task'],
                                  fields['date_begin'], 1, '',
                                  '', self.image_links.get('cancelled_img'),
                                  '', self.image_links.get('mark_time_img'),
                                  '', self.image_links.get('executed')]

                    # Заполняем поля карточек и форм данными
                    result_cod += self.fill_field_form(path_file, list_field, 0)
                return result_cod
            else:
                return self.get_processed_string('<h3>Нет данных по задаче</h3>', 0)
        # Генерация кода сохраненной плановой работы
        elif status == 1:
            # Получаем словарь с полями задачи, к которой привязана плановая работа
            plan_work_dict = self.cr.db.get_one_plan_work(id_object)

            if plan_work_dict:
                class_form = 'block_mini_form'
                if plan_work_dict['type_task'] == 1:
                    class_form = 'block_mini_form ' + 'urgent-important'
                elif plan_work_dict['type_task'] == 3:
                    class_form = 'block_mini_form ' + 'urgent-unimportant'
                elif plan_work_dict['type_task'] == 2:
                    class_form = 'block_mini_form ' + 'non-urgent-important'
                elif plan_work_dict['type_task'] == 4:
                    class_form = 'block_mini_form ' + 'non-urgent-unimportant'

                # Данные по задаче из словаря выставляем в список в порядке их вставки в шаблон карточки
                list_field = [class_form, 'Плановая работа', self.image_links.get('planned_time_img'),
                              self.image_links.get('close_img'),
                              'updatePlanWork(' + str(plan_work_dict.get('id')) + ', ' +
                              str(plan_work_dict.get('time_fact_work')) +
                              ', ' + str(plan_work_dict.get('id_task')) + ')',
                              self.image_links.get('save_img'),
                              'deletePlanWorkFromRegistry(' + str(plan_work_dict.get('id')) + ')',
                              self.image_links.get('delete_img'),
                              str(plan_work_dict.get('id')), plan_work_dict['name_project'],
                              plan_work_dict['name_stage'],
                              DT.date.strftime(DT.datetime.strptime(plan_work_dict['date_begin'], '%Y-%m-%d').date(),
                                               '%d.%m.%Y') if plan_work_dict['date_begin'] != '' else
                              plan_work_dict['date_begin'],
                              DT.date.strftime(DT.datetime.strptime(plan_work_dict['date_end_plan'], '%Y-%m-%d').date(),
                                               '%d.%m.%Y') if plan_work_dict['date_end_plan'] != '' else
                              plan_work_dict['date_end_plan'],
                              plan_work_dict['time_fact'], plan_work_dict['time_plan'], plan_work_dict['id'],
                              plan_work_dict['content_task'],
                              plan_work_dict['date_plan'], plan_work_dict['time_plan_work'],
                              plan_work_dict['planned_work'],
                              'deletePlanWorkFromRegistry(' + str(plan_work_dict.get('id')) + ')',
                              self.image_links.get('cancelled_img'),
                              'do_time_stamp_for_plan_work(' + str(plan_work_dict.get('id_task')) + ')',
                              self.image_links.get('mark_time_img'),
                              'do_execution_plan_work(' + str(plan_work_dict.get('id_task')) + ', ' +
                              str(plan_work_dict.get('id')) + ')',
                              self.image_links.get('executed')]

                # Заполняем поля карточек и форм данными
                result_cod += self.fill_field_form(path_file, list_field, 0)
                return result_cod
            else:
                return self.get_processed_string('<h3>Нет данных по задаче</h3>', 0)

    # ****************МЕТОДЫ ОТРИСОВКИ ОТМЕТОК ВРЕМЕНИ*****************
    def get_list_task_time_stamps(self, path_file, indent, type_object, id_object):
        """ Генерирует код списка отметок времени для окна right на страницах """
        result_cod = ''

        # Получаем список словарей с полями задач
        list_dict = self.cr.get_list_time_stamps(type_object, id_object)

        if list_dict:
            result_cod += '\n<div id="insert_time_stamp">\n</div>'
            for fields in list_dict:
                class_card = 'time_stamp_card'

                if fields['type_task'] == 1:
                    class_card = 'time_stamp_card ' + 'urgent-important'
                elif fields['type_task'] == 3:
                    class_card = 'time_stamp_card ' + 'urgent-unimportant'
                elif fields['type_task'] == 2:
                    class_card = 'time_stamp_card ' + 'non-urgent-important'
                elif fields['type_task'] == 4:
                    class_card = 'time_stamp_card ' + 'non-urgent-unimportant'

                image_status = self.image_links['mark_time_img']
                title_status = 'Сохраненная отметка времени'

                # Данные по задаче из словаря выставляем в список в порядке их вставки в шаблон карточки
                list_field = [
                    fields['id'], class_card, fields['id'], title_status, image_status, fields['id_project'],
                    fields['name_project'], fields['id_task'],  fields['content_task'],
                    DT.date.strftime(DT.datetime.strptime(fields['date'], '%Y-%m-%d').date(),
                                     '%d.%m.%Y') if fields['date'] != '' else fields['date'],
                    fields['time'], fields['completed_work'], fields['id'], self.image_links['delete_img']
                ]

                # Заполняем поля карточек и форм данными
                result_cod += self.fill_field_form(path_file, list_field, indent)
            return result_cod
        else:
            return self.get_processed_string('<h3>Отметок времени нет</h3>', indent)

    def get_update_list_task_time_stamps(self, id_time_stamp):
        """ Генерирует код измененной отметки времени для окна right на страницах """
        result_cod = ''

        # Получаем список словарей с полями задач
        fields = self.cr.db.get_one_time_stamp(id_time_stamp)

        class_card = 'time_stamp_card'

        if fields['type_task'] == 1:
            class_card = 'time_stamp_card ' + 'urgent-important'
        elif fields['type_task'] == 3:
            class_card = 'time_stamp_card ' + 'urgent-unimportant'
        elif fields['type_task'] == 2:
            class_card = 'time_stamp_card ' + 'non-urgent-important'
        elif fields['type_task'] == 4:
            class_card = 'time_stamp_card ' + 'non-urgent-unimportant'

        image_status = self.image_links['mark_time_img']
        title_status = 'Сохраненная отметка времени'

        # Данные по задаче из словаря выставляем в список в порядке их вставки в шаблон карточки
        list_field = [
            fields['id'], class_card, fields['id'], title_status, image_status, fields['id_project'],
            fields['name_project'], fields['id_task'], fields['content_task'], fields['date'], fields['time'],
            fields['completed_work'], fields['id'], self.image_links['delete_img']
        ]

        # Заполняем поля карточек и форм данными
        result_cod += self.fill_field_form(self.TasksPageDictionary2.get('time_stamps')[1][0], list_field, 8)

        # Удаляем первую и последнюю строку, т.к. они уже есть на странице
        list_str = result_cod.split('\n')
        list_str.pop(0)
        list_str.pop(len(list_str) - 1)
        result_cod = ''
        for one_string in list_str:
            result_cod += one_string + '\n'

        return result_cod

    def get_header_time_stamp_list_cod(self, path_file):
        """ Изввлекает код заголовка для реестра отметок времени """
        result_cod = ''
        name = ''
        condition = f'id={self.cr.global_parameters.get("id_object")}'
        if self.cr.global_parameters.get('type_filter_time_stamps_list') == 'task':
            name = self.cr.db.request_select_data('Tasks', 'content_task', condition)[0][0]
            name = 'Задача ' + '№' + str(self.cr.global_parameters.get("id_object")) + ': ' + name
        elif self.cr.global_parameters.get('type_filter_time_stamps_list') == 'project':
            name = self.cr.db.request_select_data('Projects', 'name_project', condition)[0][0]
            name = 'Проект ' + '№' + str(self.cr.global_parameters.get("id_object")) + ': ' + name
        list_field = [self.image_links.get('close_img'), name, name]
        # Заполняем поля карточек и форм данными
        result_cod += self.fill_field_form(path_file, list_field, 4)
        return result_cod

    def get_time_stamp_form_cod(self, path_file, id_object, status=0):
        """ Генерируем код формы отметки времени """
        result_cod = ''
        list_field = list()

        # Генерация кода новой отметки времени
        if status == 0:
            # Получаем словарь с полями задачи, к которой привязана плановая работа
            list_dict = self.cr.get_list_task(id_object)

            if list_dict:
                for fields in list_dict:
                    class_form = 'block_mini_form'
                    if fields['type_task'] == 1:
                        class_form = 'block_mini_form ' + 'urgent-important'
                    elif fields['type_task'] == 3:
                        class_form = 'block_mini_form ' + 'urgent-unimportant'
                    elif fields['type_task'] == 2:
                        class_form = 'block_mini_form ' + 'non-urgent-important'
                    elif fields['type_task'] == 4:
                        class_form = 'block_mini_form ' + 'non-urgent-unimportant'

                    # today_date = self.cr.db.todayDate()

                    # Данные по задаче из словаря выставляем в список в порядке их вставки в шаблон карточки
                    list_field = [class_form,  'Новая отметка времени', self.image_links.get('new_img'),
                                  self.image_links.get('close_img'),
                                  'saveNewTimeStampForm(' + str(fields['id']) + ')', self.image_links.get('save_img'),
                                  'close_mini_form()', self.image_links.get('delete_img'),
                                  '_', fields['name_project'], fields['name_stage'], fields['date_begin'],
                                  fields['date_end_plan'],
                                  fields['time_fact'], fields['time_plan'], fields['id'], fields['content_task'],
                                  '', 1, '']
            else:
                return self.get_processed_string('<h3>Нет данных по задаче</h3>', 0)
        elif status == 1:
            # Получаем словарь с полями задачи, к которой привязана плановая работа
            time_stamp_dict = self.cr.db.get_one_time_stamp(id_object)

            if time_stamp_dict:
                class_form = 'block_mini_form'
                if time_stamp_dict['type_task'] == 1:
                    class_form = 'block_mini_form ' + 'urgent-important'
                elif time_stamp_dict['type_task'] == 3:
                    class_form = 'block_mini_form ' + 'urgent-unimportant'
                elif time_stamp_dict['type_task'] == 2:
                    class_form = 'block_mini_form ' + 'non-urgent-important'
                elif time_stamp_dict['type_task'] == 4:
                    class_form = 'block_mini_form ' + 'non-urgent-unimportant'

                # Данные по задаче из словаря выставляем в список в порядке их вставки в шаблон карточки
                list_field = [class_form, 'Сохраненная отметка времени', self.image_links.get('mark_time_img'),
                              self.image_links.get('close_img'),
                              'updateTimeStamp(' + str(time_stamp_dict['id']) + ', ' +
                              str(time_stamp_dict['id_task']) + ')',
                              self.image_links.get('save_img'),
                              'deleteTimeStamp(' + str(time_stamp_dict['id']) + ')',
                              self.image_links.get('delete_img'),
                              str(time_stamp_dict['id']), time_stamp_dict['name_project'],
                              time_stamp_dict['name_stage'],
                              DT.date.strftime(DT.datetime.strptime(time_stamp_dict['date_begin'], '%Y-%m-%d').date(),
                                               '%d.%m.%Y') if time_stamp_dict['date_begin'] != '' else
                              time_stamp_dict['date_begin'],
                              DT.date.strftime(DT.datetime.strptime(time_stamp_dict['date_end_plan'],
                                                                    '%Y-%m-%d').date(), '%d.%m.%Y') if
                              time_stamp_dict['date_end_plan'] != '' else time_stamp_dict['date_end_plan'],
                              time_stamp_dict['time_fact_work'],
                              time_stamp_dict['time_plan_work'], time_stamp_dict['id'], time_stamp_dict['content_task'],
                              time_stamp_dict['date'], time_stamp_dict['time'], time_stamp_dict['completed_work']]

            else:
                return self.get_processed_string('<h3>Нет данных по отметке</h3>', 0)

        # Заполняем поля карточек и форм данными
        result_cod += self.fill_field_form(path_file, list_field, 0)
        return result_cod

    # ****************МЕТОДЫ ОТРИСОВКИ РАСКРЫВАЮЩИХСЯ СПИСКОВ*****************
    @staticmethod
    def get_code_select_types(type_task):
        """ Извлечение html кода опций для выбора типа задачи """
        insert_types = ['', '', '', '']
        insert_types[type_task - 1] = 'selected'
        html_cod = f""" 
            <option value="1" {insert_types[0]}>"A" Срочная важная</option>\n
            <option value="2" {insert_types[1]}>"B" Несрочная важная</option>\n
            <option value="3" {insert_types[2]}>"C" Срочная неважная</option>\n
            <option value="4" {insert_types[3]}>"D" Несрочная неважная</option>\n
        """
        return html_cod

    def get_code_select_project(self, id_project):
        """ Извлечение html кода опций для выбора проекта """
        html_cod = ''
        list_project = self.cr.db.request_select_data('Projects', 'id, name_project, status_project')
        if list_project:
            for project in list_project:
                if project[0] == id_project:
                    selected = 'selected'
                else:
                    selected = ''

                color = '#000000'
                if project[2] == 2:
                    color = '008000'
                elif project[2] == 3:
                    color = 'ff0000'

                html_cod += f' <option value="{project[0]}" style="{color}" {selected}>{project[1]}</option>\n'
        else:
            html_cod = ''
        return html_cod

    def get_code_filter_select_project(self):
        """ Извлечение html кода опций для выбора фильтра проекта в реестре задач """
        html_cod = ''

        selected = 'selected'
        if self.cr.global_parameters.get('filter_project') == -1:
            html_cod += f'<option value="-1" {selected}>Все задачи</option>'
        else:
            html_cod += f'<option value="-1">Все проекты</option>'

        if self.cr.global_parameters.get('filter_project') == 0:
            html_cod += f'<option value="0" {selected}>Без проектов</option>'
        else:
            html_cod += f'<option value="0">Без проектов</option>'

        html_cod += self.get_code_select_project(self.cr.global_parameters.get('filter_project'))

        return html_cod

    def get_code_filter_status_task(self):
        """ Извлечение html кода опций для выбора фильтра реестра задач по статусу """
        html_cod = ''
        selected = 'selected'
        if self.cr.global_parameters.get('filter_type_task') == 1:
            html_cod += f'<option value="1" {selected}>В работе</option>'
        else:
            html_cod += f'<option value="1">В работе</option>'

        if self.cr.global_parameters.get('filter_type_task') == 2:
            html_cod += f'<option value="2" {selected}>Все</option>'
        else:
            html_cod += f'<option value="2">Все</option>'

        if self.cr.global_parameters.get('filter_type_task') == 3:
            html_cod += f'<option value="3" {selected}>Выполненные</option>'
        else:
            html_cod += f'<option value="3">Выполненные</option>'

        if self.cr.global_parameters.get('filter_type_task') == 4:
            html_cod += f'<option value="4" {selected}>Отклоненные</option>'
        else:
            html_cod += f'<option value="4">Отклоненные</option>'

        return html_cod

    def get_code_filter_status_project(self):
        """ Извлечение html кода опций для выбора фильтра реестра проектов по статусу """
        html_cod = ''
        selected = 'selected'
        if self.cr.global_parameters.get('filter_list_project') == 1:
            html_cod += f'<option value="1" {selected}>В работе</option>'
        else:
            html_cod += f'<option value="1">В работе</option>'

        if self.cr.global_parameters.get('filter_list_project') == 2:
            html_cod += f'<option value="2" {selected}>Все</option>'
        else:
            html_cod += f'<option value="2">Все</option>'

        if self.cr.global_parameters.get('filter_list_project') == 3:
            html_cod += f'<option value="3" {selected}>Выполненные</option>'
        else:
            html_cod += f'<option value="3">Выполненные</option>'

        if self.cr.global_parameters.get('filter_list_project') == 4:
            html_cod += f'<option value="4" {selected}>Отклоненные</option>'
        else:
            html_cod += f'<option value="4">Отклоненные</option>'

        return html_cod
