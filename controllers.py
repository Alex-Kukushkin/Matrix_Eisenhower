import model as DB
import views as VP
import urllib.parse


class ControllersResponses:
    def __init__(self):
        self.db = DB.DataBases(self)
        self.vp = VP.ViewsPages()
        self.buffer_params = list()
        self.URLS = {
            '/': lambda: self.draw_matrix_Eisenhower_page(),
            '/Tasks': lambda: self.draw_tasks_page(),
            '/Projects': lambda: self.draw_projects_page(),

            '/CreateTask': lambda: self.create_task(self.buffer_params),
            '/OpenTaskForm': lambda: self.open_task_form(self.buffer_params),
            '/UpdateTask': lambda: self.update_task(self.buffer_params),
            '/DeleteTask': lambda: self.delete_task(self.buffer_params),
            '/UpdateTaskCard': lambda: self.update_task_card(self.buffer_params),

            '/OpenNewPlanWorkForm': lambda: self.open_new_plan_work_form(self.buffer_params),
            '/OpenPlanWorkForm': lambda: self.open_plan_work_form(self.buffer_params),
            '/SaveNewPlanWorkForm': lambda: self.save_new_plan_work_form(self.buffer_params),
            '/UpdatePlanWorkForm': lambda: self.update_plan_work_form(self.buffer_params),
            '/DeletePlanWorkFromRegistry': lambda: self.delete_plan_work_from_registry(self.buffer_params),

            '/OpenNewTimeStampForm': lambda: self.open_new_time_stamp_form(self.buffer_params),
            '/OpenTimeStampForm': lambda: self.open_time_stamp_form(self.buffer_params),
            '/SaveNewTimeStampForm': lambda: self.save_new_time_stamp_form(self.buffer_params),
            '/DeleteTimeStamp': lambda: self.delete_time_stamp(self.buffer_params),
            '/UpdateTimeStamp': lambda: self.update_time_stamp(self.buffer_params),
            '/UpdateTimeStampCard': lambda: self.update_time_stamp(self.buffer_params),

            '/OpenProjectForm': lambda: self.open_project_form(self.buffer_params),
            '/UpdateProject': lambda: self.update_project(self.buffer_params),
            '/CreateProject': lambda: self.create_project(self.buffer_params),
            '/CloseProject': lambda: self.close_project(),
            '/DeleteProject': lambda: self.delete_project(self.buffer_params),
            '/ChangeFilterProjects': lambda: self.update_projects_list(self.buffer_params),

            '/DrawListTimeStamp': lambda: self.draw_list_time_stamp(self.buffer_params),
            '/CloseListTimeStamps': lambda: self.vp.generate_page_code_recursion(
                self.vp.TasksPageDictionary2.get('right')[1][0], 4, self.vp.TasksPageDictionary2),
            '/ChangeFilterTask': lambda: self.update_task_list(self.buffer_params),

        }
        self.vp.cr = self

        """ 
        Список ключей используемых глобальных параметров:
        'type_filter_time_stamps_list' - тип объекта фильтрации отметок времени 
            (по задаче 'tack' или проекту 'project');
        'id_object' - id объекта фильтрации отметок времени (по задаче или проекту);
        'filter_type_task' - фильтр по статусам задачи
        'filter_project' - фильтр задач по связи с проектами
        'id_task' - id задачи при переходе из других разделов
        'number_page' - индентификатор текущей страницы: 0 - Матрица эйзенхауэра, 1 - страница редактирования задачи,
            2 - таблица проектов
        """
        self.global_parameters = {'id_task': 0, 'filter_type_task': 1, 'filter_project': -1, 'filter_list_project': 1,
                                  'number_page': 0}

    # ****************МЕТОДЫ ОБРАБОТКИ ЗАПРОСОВ***********************
    @staticmethod
    def parse_request(request):
        """ Парсим запрос клиента, извлекаем метод запроса и URL """
        parsed = request.split()
        method = parsed[0]
        url = ''
        list_params = list()

        if method == 'GET':
            url_and_parameters = parsed[1].split('?')
            url = url_and_parameters[0]

            if len(url_and_parameters) == 2:
                parameters = urllib.parse.unquote(url_and_parameters[1])
                list_params = ControllersResponses.parse_parameters(parameters)

        elif method == 'POST':
            url = parsed[1]
            parameters = urllib.parse.unquote(parsed[len(parsed) - 1])
            list_params = ControllersResponses.parse_parameters(parameters)

        return method, url, list_params

    @staticmethod
    def parse_parameters(parameters):
        """ Парсит строку с параметрами на отдельные переменные, пакует их в список, извлекает список """
        list_params = list()
        parameters = parameters.split('||*||')
        for param in parameters:
            list_params.append(param)
        return list_params

    def generate_headers(self, method, url):
        """ Генерируем заголовок ответа """
        if method != 'GET' and method != 'POST':
            return 'HTTP/1.1 405 Method not allowed\n\n', 405

        if url not in self.URLS:
            return 'HTTP/1.1 404 Not found\n\n', 404

        return 'HTTP/1.1 200 OK\n\n', 200

    def generate_content(self, code, url):
        """ Генерируем код страницы """
        if code == 404:
            return '<h1>404</h1><p>NOT FOUND</p>'
        if code == 405:
            return '<h1>405</h1><p>NOT ALLOWED</p>'

        return self.URLS[url]()

    def generate_response(self, request):
        """ Генерируем ответ на запрос клиента """
        method, url, params = self.parse_request(request)
        self.buffer_params = params
        headers, code = self.generate_headers(method, url)
        body = self.generate_content(code, url)

        return (headers + body).encode()

    # ****************МЕТОДЫ ПОСТРОЕНИЯ ОСНОВНЫХ СТРАНИЦ*****************
    def draw_matrix_Eisenhower_page(self):
        """ Извлекает код для страница матрицы Эйзенхауэра"""
        self.global_parameters['number_page'] = 0
        return self.vp.generate_page_code_recursion(self.vp.general_template, 0, self.vp.MatrixEisenhowerDictionary2)

    def draw_tasks_page(self):
        """ Извлекает код для страницы создания и редактирования задач """
        self.global_parameters['number_page'] = 1
        return self.vp.generate_page_code_recursion(self.vp.general_template, 0, self.vp.TasksPageDictionary2)

    def draw_projects_page(self):
        """ Извлекает код для страницы создания и редактирования задач """
        self.global_parameters['number_page'] = 2
        return self.vp.generate_page_code_recursion(self.vp.general_template, 0, self.vp.ProjectPageDictionary2)

    # ****************ПРОЕКТЫ*****************
    def create_project(self, list_params):
        """ Создать новый проект """
        # Сохранение проекта в БД
        self.db.add_new_project(list_params)
        # Загрузка реестра проектов
        return self.close_project()

    def update_project(self, list_params):
        """ Обновить проект проект """
        if list_params and type(list_params) == list:
            id_project = list_params[0]
            list_params.pop(0)

            # Обновление проекта в БД
            self.db.update_project(list_params, id_project)

            # Загрузка реестра проектов
            return self.close_project()

    def open_project_form(self, list_params):
        """ Открываем форму создания нового проекта """
        if list_params and type(list_params) == list:
            return self.vp.get_project_form_cod(self.vp.ProjectPageDictionary2.get('project_form_main')[1][0], 8,
                                                list_params[0])

    def close_project(self):
        """ Отрисовка реестра проектоа после закрытия формы проекта """
        cod = self.vp.generate_page_code_recursion(self.vp.ProjectPageDictionary2.get('main')[1][0], 8,
                                                   self.vp.ProjectPageDictionary2)
        return cod

    def get_list_projects(self, id_project=0):
        """ Возвращает список словарей полей для отрисовки реестра проектов """
        list_dict = list()
        # Запрашиваем список всех задач (в будущем с примененным фильтром)
        if id_project == 0:
            list_project = self.db.get_list_projects()
        else:
            condition_fields = f'id={id_project}'
            list_project = self.db.request_select_data('Projects', '*', condition_fields)

        if list_project:
            # Заполняем поля в словарь
            for project in list_project:
                task_dict = {'id': project[0], 'name_project': project[1], 'content_project': project[2],
                             'date_begin': project[3], 'date_end_plan': project[4], 'date_end_fact': project[5],
                             'time_plan': project[6], 'time_fact': project[7], 'execution_comment': project[8],
                             'status_project': project[9]
                             }
                if len(project) == 11:
                    task_dict['list_stage'] = project[10]

                list_dict.append(task_dict)

        return list_dict

    def delete_project(self, list_params):
        """ Удаление проекта """
        if list_params and type(list_params) == list:
            id_project = list_params[0]

            # Если с проектом связаны задачи - обнуляем поля проекта в связанных задачах
            list_task_for_project = self.db.request_select_data('Tasks', 'id', f'id_project={id_project}')
            if list_task_for_project:
                for task in list_task_for_project:
                    self.db.update_one_field('Tasks', 'id_project', 0, task[0])

            # Удаляем проект
            self.db.delete_note('Projects', id_project)

            # Загрузка реестра проектов
            return self.close_project()

    def update_projects_list(self, list_params):
        """ Обновление реестра проектов при изменении значения фильтров """
        if list_params and type(list_params) == list and len(list_params) == 1:
            self.global_parameters['filter_list_project'] = int(list_params[0])
            return self.vp.get_list_projects_code(self.vp.ProjectPageDictionary2.get('list_projects')[1][0], 6)

    # ****************ЗАДАЧИ*****************
    def create_task(self, list_params):
        """ Создать новую задачу """
        # Сохранение задачи в БД
        last = self.db.add_new_task(list_params)
        # Вставка новой задачи в реестр
        insert_task = self.vp.get_list_task_code(self.vp.TasksPageDictionary2.get('tasks')[1][0], 0, last)

        return insert_task

    def open_task_form(self, list_params):
        """ Открытие сохраненной задачи """
        if list_params and type(list_params) == list:
            # Если мы находимся на странице задач то просто отрываем задачу на основной панели
            if self.global_parameters.get('number_page') == 1:
                insert_task_form = self.vp.get_task_cod_form(
                    self.vp.TasksPageDictionary2.get('task_form_main')[1][0], 8, int(list_params[0]))
                return insert_task_form
            # Если мы находимся НЕ на странице задач то переходим на страницу задач и отрываем задачу на основной панели
            else:
                self.global_parameters['id_task'] = int(list_params[0])
                cod_page = self.draw_tasks_page()
                self.global_parameters['id_task'] = 0

                return cod_page

    def update_task_card(self, list_params):
        """Обновление одной задачи в реестре"""
        if list_params:
            update_cod = self.vp.get_update_list_task_code(list_params[0])
            return update_cod

    def delete_task(self, id_task):
        """ Удаление задачи и связанных с ней плановых работ """
        if id_task and type(id_task) == list:
            condition = f'id_task={int(id_task[0])}'

            # Удаляем связанные плановые работы
            data = self.db.request_select_data('PlanWork', 'id', condition)
            if data:
                for plan_work in data:
                    self.db.delete_note('PlanWork', plan_work[0])

            # Удаляем связанные отметки времени
            data = self.db.request_select_data('TimeStamp', 'id', condition)
            if data:
                for plan_work in data:
                    self.db.delete_note('TimeStamp', plan_work[0])

            # Пересчитываем время, потраченное на проект
            condition = f'id={int(id_task[0])}'
            data2 = self.db.request_select_data('Tasks', 'id_project, time_fact', condition)[0]
            if data and data2 and data[0] != 0 and data2[1] != 0:
                self.db.recalculate_time_project(data[0])

            # Удаляем задачу и отрисовываем форму новой задачи
            self.db.delete_note('Tasks', int(id_task[0]))
            cod_task_form = self.open_task_form([0])

            return cod_task_form

    def update_task(self, list_params):
        """ Сохранить внесенные в задачу изменения """
        id_task = int(list_params[0])
        id_project_old = self.db.request_select_data('Tasks', 'id_project')[0][0]
        id_project_new = int(list_params[9])

        list_params.pop(0)
        self.db.update_task(list_params, id_task)

        # Если изменился проект задачи, то пересчитываем время по проектам
        if id_project_old != id_project_new:
            if id_project_old != 0:
                self.db.recalculate_time_project(id_project_old)
            if id_project_new != 0:
                self.db.recalculate_time_project(id_project_new)

        cod_task_form = self.open_task_form([0])
        return cod_task_form

    def get_list_task(self, id_task=0):
        """ Возвращает список словарей полей для отрисовки реестра задач """
        list_dict = list()
        # Запрашиваем список всех задач с примененными фильтрами по статусу и проектам
        list_tasks = self.db.get_list_task(id_task)

        if list_tasks:
            # Заполняем поля в словарь
            for task in list_tasks:
                task_dict = {'id': task[0], 'content_task': task[1], 'type_task': task[2],
                             'date_begin': task[3], 'date_end_plan': task[4], 'date_end_fact': task[5],
                             'time_plan': task[6], 'time_fact': task[7], 'execution_comment': task[8],
                             'id_project': task[9], 'id_stage_project': task[10], 'status_stage': task[11],
                             'name_project': task[12], 'name_stage': task[13]
                             }

                list_dict.append(task_dict)

        return list_dict

    def update_task_list(self, list_params):
        """ Обновление реестра задач при изменении значения фильтров """
        if list_params and type(list_params) == list and len(list_params) == 2:
            if list_params[0] == 'task':
                self.global_parameters['filter_type_task'] = int(list_params[1])
            else:
                self.global_parameters['filter_project'] = int(list_params[1])

            return self.vp.get_list_task_code(self.vp.TasksPageDictionary2.get('tasks')[1][0], 6)

    # ****************ПЛАНОВЫЕ РАБОТЫ*****************
    def save_new_plan_work_form(self, list_params):
        """ Сохранить новую плановую работу """
        # Сохранение плановой работы в БД
        last = self.db.add_new_plan_work(list_params)
        # Вставка новой задачи в реестр
        insert_plan_work = self.vp.get_list_plan_work_code(
            self.vp.MatrixEisenhowerDictionary2.get('list_plan_works1')[1][0], 0, 0, last)

        return insert_plan_work

    def update_plan_work_form(self, list_params):
        """ Обновляем отметку времени (сохраняем изменения) """
        if list_params and len(list_params) == 6:
            id_plan_work = list_params[0]
            list_params.pop(0)
            self.db.update_plan_work(list_params, id_plan_work)

            update_plan_work = self.vp.get_update_list_plan_work_code(int(id_plan_work))

            return update_plan_work

    def open_new_plan_work_form(self, list_params):
        """ Открытие новой формы плановой работы """
        if list_params and type(list_params) == list:
            return self.vp.get_plan_work_form_cod(self.vp.TasksPageDictionary2.get('mini_form')[1][1], list_params[0])

    def open_plan_work_form(self, list_params):
        """ Открытие сохраненной формы плановой работы """
        if list_params and type(list_params) == list:
            return self.vp.get_plan_work_form_cod(self.vp.TasksPageDictionary2.get('mini_form')[1][1],
                                                  list_params[0], 1)

    def get_list_plan_works(self, type_task, id_plan_work=0):
        """ Возвращает список словарей полей для отрисовки реестра карточек
         планируемых работ """
        list_dict = list()

        # Запрашиваем список всех плановых работ (в будущем с примененным фильтром даты)
        if type_task != 0:
            list_plan_works = self.db.get_list_plan_works(type_task)
            if list_plan_works:
                # Заполняем поля в словарь
                for plan_work in list_plan_works:
                    plan_work_dict = {'id': plan_work[0], 'planned_work': plan_work[1],
                                      'date_plan': plan_work[2], 'time_plan_work': plan_work[3],
                                      'time_fact_work': plan_work[4], 'id_task': plan_work[5],
                                      'content_task': plan_work[6], 'type_task': plan_work[7],
                                      'date_begin': plan_work[8], 'date_end_plan': plan_work[9],
                                      'time_plan': plan_work[10], 'time_fact': plan_work[11],
                                      'id_project': plan_work[12], 'id_stage_project': plan_work[13],
                                      'name_project': plan_work[14], 'name_stage': plan_work[15]}

                    list_dict.append(plan_work_dict)
        elif id_plan_work != 0:
            list_plan_works = self.db.get_one_plan_work(id_plan_work)
            if list_plan_works:
                list_dict.append(list_plan_works)

        return list_dict

    def delete_plan_work_from_registry(self, id_plan_work):
        """ Удаление плановой работы из матрицы Эйзенхауэра """
        if id_plan_work and type(id_plan_work) == list:
            self.db.delete_note('PlanWork', int(id_plan_work[0]))

            return ''

    # ****************ОТМЕТКИ ВРЕМЕНИ*****************
    def save_new_time_stamp_form(self, list_params):
        """ Сохранить новую отметку времени """
        # Сохранение отметки времени в БД
        self.db.add_new_time_stamp(list_params)
        self.db.recalculate_time_task(list_params[3])

        return ''

    def update_time_stamp(self, list_params):
        """ Обновляем отметку времени (сохраняем изменения) """
        if list_params and len(list_params) == 5:
            id_time_stamp = list_params[0]
            list_params.pop(0)
            self.db.update_time_stamp(list_params, id_time_stamp)
            self.db.recalculate_time_task(list_params[3])

            cod_card = self.vp.get_update_list_task_time_stamps(id_time_stamp)

            return cod_card

    def delete_time_stamp(self, list_params):
        """ Удаляем отметку времени """
        condition = f'id={list_params[0]}'
        id_task = self.db.request_select_data('TimeStamp', 'id_task', condition)[0][0]

        # Удаление отметки времени в БД
        self.db.delete_note('TimeStamp', list_params[0])
        self.db.recalculate_time_task(id_task)

        return ''

    def draw_list_time_stamp(self, list_params):
        """ Отрисовка списка отметок времени в правой панели """
        if list_params and type(list_params) == list and list_params and len(list_params) == 2:
            self.global_parameters['type_filter_time_stamps_list'] = list_params[0]
            self.global_parameters['id_object'] = int(list_params[1])

            return self.vp.generate_page_code_recursion(self.vp.TasksPageDictionary2.get('block_time_stamps')[1][0], 4,
                                                        self.vp.TasksPageDictionary2)

    def open_new_time_stamp_form(self, list_params):
        if list_params and type(list_params) == list:
            return self.vp.get_time_stamp_form_cod(self.vp.TasksPageDictionary2.get('mini_form')[1][0], list_params[0])

    def open_time_stamp_form(self, list_params):
        if list_params and type(list_params) == list:
            return self.vp.get_time_stamp_form_cod(self.vp.TasksPageDictionary2.get('mini_form')[1][0],
                                                   list_params[0], 1)

    def get_list_time_stamps(self, type_object, id_object):
        """ Возвращает список словарей полей для отрисовки реестра карточек
        отметок времени или один словарь для отрисовки формы отметок времени """
        list_dict = list()
        list_time_stamps = self.db.get_list_time_stamps(type_object, id_object)
        if list_time_stamps:
            # Заполняем поля в словарь
            for time_stamp in list_time_stamps:
                time_stamps_dict = {
                    'id': time_stamp[0], 'completed_work': time_stamp[1],
                    'date': time_stamp[2], 'time': time_stamp[3],
                    'id_task': time_stamp[4],
                    'content_task': time_stamp[5], 'type_task': time_stamp[6], 'status_stage': time_stamp[7],
                    'id_project': time_stamp[8], 'id_stage_project': time_stamp[9],
                    'name_project': time_stamp[10], 'name_stage': time_stamp[11]}

                list_dict.append(time_stamps_dict)
        return list_dict
