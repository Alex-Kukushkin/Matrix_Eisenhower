import os.path as OP
import sqlite3
import datetime as DT


class DataBases:
    def __init__(self, cr):
        # Сегодняшняя дата
        self.__today = DT.date.today()
        self.cr = cr

        if not OP.exists('templates/DB/MatrixEisenhower.db'):
            # Создаем Базу данных при первом входе
            with sqlite3.connect('templates/DB/MatrixEisenhower.db') as con:
                cur = con.cursor()
                # ===================таблица ПРОЕКТОВ=====================================
                cur.execute('''CREATE TABLE IF NOT EXISTS Projects (
                    id integer primary key,
                    name_project text, content_project text, date_begin  date,
                    date_end_plan date, date_end_fact date,
                    time_plan real, time_fact real,  execution_comment text, status_project integer)''')
                con.commit()
                print('OK! Таблица Проектов создана')

                # ===================таблица ЭТАПОВ ПРОЕКТОВ=====================================
                cur.execute('''CREATE TABLE IF NOT EXISTS StageProjects (id integer primary key,
                    name_stage text, content_stage text, date_begin  date, date_end_plan date,
                    date_end_fact date, time_plan real, time_fact real,  execution_comment text,
                    id_project integer references Projects(id), status_stage integer)''')
                con.commit()
                print('OK! Таблица Этапов проектов создана')

                # ===================таблица ЗАДАЧ=====================================
                cur.execute('''CREATE TABLE IF NOT EXISTS Tasks (id integer primary key,
                    content_task text, type_task integer, date_begin  date, date_end_plan date,
                    date_end_fact date, time_plan real, time_fact real, execution_comment text,
                    id_project integer references Projects(id),
                    id_stage_project  integer references StageProjects(id), status_stage integer)''')
                con.commit()
                print('OK! Таблица Задач создана')

                # ===================таблица ЗАПЛАНИРОВАННЫХ РАБОТ===================
                cur.execute('''CREATE TABLE IF NOT EXISTS PlanWork (id integer primary key,
                    planned_work text, date_plan date, time_plan real, time_work_fact real,
                    id_task  integer references Tasks(id))''')
                con.commit()
                print('OK! Таблица Запланированных работ создана')

                # ===================таблица ОТМЕТОК ВРЕМЕНИ============================
                cur.execute('''CREATE TABLE IF NOT EXISTS TimeStamp (id integer primary key,
                    completed_work text, date date, time real,
                    id_task integer references Tasks(id))''')
                con.commit()
                print('OK! Таблица Отметок времени создана')

        else:
            print('OK! База данных существовала')

    @property
    def todayDate(self):
        return self.__today

    @todayDate.setter
    def todayDate(self, todayDate):
        self.__today = todayDate

    # ==============================Общие методы ==========================================================
    @staticmethod
    def update_one_field(name_table, field, data, iditem, idname='id'):
        """ Запрос на обновление одного поля: path= путь к таблице, database= имя таблицы,
            field= имя обновляемого поля, data= данные для записи,
            iditem= id обновляемой записи, idname= наименования поля id в таблице  """

        with sqlite3.connect('templates/DB/MatrixEisenhower.db') as con:
            cur = con.cursor()
            request = f'UPDATE {name_table} SET {field}=? WHERE {idname}=?'
            try:
                cur.execute(request, (data, iditem))
                con.commit()
            except Exception as err:
                print('Ошибка при работе с БД:', err)

    @staticmethod
    def request_select_data(name_table, selectionfields, conditionfields=''):
        """ Запрос на отбор записей в базе данных, извлекает результат отбора:
            path= путь к таблице, database= имя таблицы, selectionfields= отбираемые Заполняется
            conditionfields= условия отбора"""

        with sqlite3.connect('templates/DB/MatrixEisenhower.db') as con:
            cur = con.cursor()

            if conditionfields == '':
                request = f'SELECT {selectionfields} FROM {name_table}'
            else:
                request = f'SELECT {selectionfields} FROM {name_table} WHERE {conditionfields}'

            try:
                cur.execute(request)
                data = cur.fetchall()
                return data
            except Exception as err:
                print('Ошибка при работе с БД:', err)

    @staticmethod
    def delete_note(name_table, id_note, idname='id'):
        """ Удаляем запись из таблицы по id: path= путь к таблице, database= имя таблицы,
            id_note= id удаляемой из таблицы записи, idname= наименования поля id в таблице"""
        with sqlite3.connect('templates/DB/MatrixEisenhower.db') as con:
            cur = con.cursor()
            request = f'DELETE FROM {name_table} WHERE {idname}=?'
            try:
                cur.execute(request, (id_note,))
                con.commit()
                print(f'Из таблицы {name_table} удалена запись: {id_note}')
            except Exception as err:
                print('Ошибка при работе с БД:', err)

    # ===============================Методы для задач===============================
    @staticmethod
    def add_new_task(data):
        """ Создание новой записи в таблице Задачи """
        normal_data = data
        with sqlite3.connect('templates/DB/MatrixEisenhower.db') as con:
            cur = con.cursor()
            cur.execute(''' INSERT INTO Tasks (content_task, type_task, date_begin,
                date_end_plan, date_end_fact, time_plan, time_fact, execution_comment,
                id_project, id_stage_project, status_stage)
                VALUES( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', normal_data)

            # Индекс добавленной  записи
            last = cur.lastrowid
            print('В БД внесена новая запись Задачи')
            con.commit()
            return last

    @staticmethod
    def update_task(data, id_task):
        """ Обновление полей задачи при изменении: data= список новых значений,
            id_task= id обновляемой в таблице записи"""
        print('update_task', data, id_task)
        with sqlite3.connect('templates/DB/MatrixEisenhower.db') as con:
            cur = con.cursor()
            data.append(id_task)
            tt = type(data)
            print(tt)
            update_data = tuple(data)

            print('update_data', update_data)
            cur.execute(''' UPDATE Tasks SET content_task=?, type_task=?, date_begin=?,
                date_end_plan=?, date_end_fact=?, time_plan=?, time_fact=?, execution_comment=?,
                id_project=?, id_stage_project=?, status_stage=?
                WHERE id=? ''', update_data)

            con.commit()
            print('В БД изменены данные по задаче')

    def get_list_task(self, id_task=0):
        """ Запрос данных для списка задач
        если id_task=0 то ищем все задачи, иначе задачу по id"""
        with sqlite3.connect('templates/DB/MatrixEisenhower.db') as con:
            cur = con.cursor()
            task_condition = ''

            if id_task != 0:
                task_condition = f' WHERE Tasks.id={id_task}'
            else:
                project_condition = ''
                task_status_condition = ''

                # Условия для фильтра задач
                # Фильтр "В работе"
                if self.cr.global_parameters.get('filter_type_task') == 1:
                    task_status_condition = f'Tasks.status_stage=1'
                # Фильтр "Выполненные"
                elif self.cr.global_parameters.get('filter_type_task') == 3:
                    task_status_condition = 'Tasks.status_stage=2'
                # Фильтр "Отклоненные"
                elif self.cr.global_parameters.get('filter_type_task') == 4:
                    task_status_condition = 'Tasks.status_stage=3'

                # Условия для фильтра проектов
                # Без проектов
                if self.cr.global_parameters.get('filter_project') == 0:
                    project_condition = f'Tasks.id_project=0'
                # Фильтр по id проекта
                elif self.cr.global_parameters.get('filter_project') not in (-1, 0):
                    project_condition = f'Tasks.id_project={self.cr.global_parameters.get("filter_project")}'

                if task_status_condition and project_condition:
                    task_condition = f'WHERE {task_status_condition} AND {project_condition}'
                elif task_status_condition and not project_condition:
                    task_condition = f'WHERE {task_status_condition}'
                elif not task_status_condition and project_condition:
                    task_condition = f'WHERE {project_condition}'

                print(self.cr.global_parameters.get('filter_type_task'), '+', task_status_condition, '+',
                      project_condition)

            request = f''' SELECT Tasks.*, 
                    COALESCE((SELECT name_project FROM Projects WHERE id=Tasks.id_project), '-'),
                    COALESCE((SELECT name_stage FROM StageProjects WHERE id=Tasks.id_stage_project), '-')
                    FROM Tasks {task_condition} '''

            try:
                cur.execute(request)
                data = cur.fetchall()
                return data
            except Exception as err:
                print('Ошибка при работе с БД:', err)

    @staticmethod
    def recalculate_time_task(id_task):
        """ Пересчет времени у задачи """
        with sqlite3.connect('templates/DB/MatrixEisenhower.db') as con:
            cur = con.cursor()

            request = f''' 
                        UPDATE Tasks SET time_fact=(SELECT sum(time) FROM TimeStamp WHERE id_task={id_task})
                        WHERE id={id_task} '''

            try:
                cur.execute(request)
                con.commit()
                condition = f'id={id_task}'
                id_project = DataBases.request_select_data('Tasks', 'id_project', condition)[0][0]
                if id_project != 0:
                    DataBases.recalculate_time_project(id_project)
            except Exception as err:
                print('Ошибка при работе с БД:', err)

    # ===============================Методы для проектов===============================
    @staticmethod
    def add_new_project(data):
        """ Создание новой записи в таблице Проекты """
        with sqlite3.connect('templates/DB/MatrixEisenhower.db') as con:
            cur = con.cursor()
            try:
                cur.execute(''' INSERT INTO Projects (name_project, content_project, date_begin,
                    date_end_plan, date_end_fact, time_plan, time_fact, execution_comment, status_project)
                    VALUES( ?, ?, ?, ?, ?, ?, ?, ?, ?)''', data)
                # Индекс добавленной  записи
                last = cur.lastrowid
                con.commit()
                print('В БД внесена новая запись Проекта')
                return last
            except Exception as err:
                print('Ошибка при работе с БД:', err)

    @staticmethod
    def update_project(data, id_project):
        """ Обновление полей проекта при изменении: data= список новых значений,
            id_project= id обновляемой в таблице записи"""
        data.append(id_project)
        update_data = tuple(data)

        with sqlite3.connect('templates/DB/MatrixEisenhower.db') as con:
            cur = con.cursor()
            try:
                cur.execute(''' UPDATE Projects SET name_project=?, content_project=?, date_begin=?,
                    date_end_plan=?, date_end_fact=?, time_plan=?, time_fact=?, execution_comment=?, status_project=?
                    WHERE id=? ''', update_data)
                con.commit()
                print(f'В БД изменены данные по Проекту: {id_project}')
            except Exception as err:
                print('Ошибка при работе с БД:', err)

    def get_list_projects(self):
        """ Запрос данных для списка проектов с примененным фильтром по статусу"""
        with sqlite3.connect('templates/DB/MatrixEisenhower.db') as con:
            cur = con.cursor()
            filter_project = self.cr.global_parameters.get('filter_list_project')
            project_condition = ''
            if filter_project != 2:
                if filter_project == 3:
                    filter_project = 2
                if filter_project == 4:
                    filter_project = 3
                project_condition = f'WHERE Projects.status_project={filter_project}'

            request = f''' SELECT Projects.*, (SELECT COUNT(*) FROM StageProjects 
                                                   WHERE StageProjects.id_project=Projects.id
                                                   ORDER BY StageProjects.date_begin DESC) 
                               FROM Projects {project_condition} 
                               ORDER BY Projects.date_begin DESC
                               '''
            try:
                cur.execute(request)
                data = cur.fetchall()
                return data

            except Exception as err:
                print('Ошибка при работе с БД:', err)

    @staticmethod
    def recalculate_time_project(id_project):
        """ Пересчет времени у задачи """
        with sqlite3.connect('templates/DB/MatrixEisenhower.db') as con:
            cur = con.cursor()
            request = f''' 
                        UPDATE Projects SET time_fact=(SELECT sum(time_fact) FROM Tasks WHERE id_project={id_project})
                        WHERE id={id_project} '''

            try:
                cur.execute(request)
                con.commit()
            except Exception as err:
                print('Ошибка при работе с БД:', err)

    # ===============================Методы для этапов проектов===============================
    @staticmethod
    def add_new_stage_project(data):
        """ Создание новой записи в таблице Этапы проекта """
        with sqlite3.connect('templates/DB/MatrixEisenhower.db') as con:
            cur = con.cursor()
            try:
                cur.execute(''' INSERT INTO StageProjects (name_stage, content_stage, date_begin,
                    date_end_plan, date_end_fact, time_plan, time_fact, execution_comment, id_project, status_stage)
                    VALUES( ?, ?, ?, ?, ?, ?, ?, ?, ?)''', data)

                con.commit()
                print('В БД внесена новая запись Этапа проекта')
            except Exception as err:
                print('Ошибка при работе с БД:', err)

    @staticmethod
    def update_stage_project(data, id_stage):
        """ Обновление полей этапа проекта при изменении: data= список новых значений,
            id_stage= id обновляемой в таблице записи"""
        with sqlite3.connect('templates/DB/MatrixEisenhower.db') as con:
            cur = con.cursor()
            try:
                cur.execute(''' UPDATE StageProjects SET name_stage=?, content_stage=?,
                    date_begin=?, date_end_plan=?, date_end_fact=?, time_plan=?,
                    time_fact=?, execution_comment=?, id_project=?, status_stage=?
                    WHERE id=? ''', (data.append(id_stage)))

                con.commit()
                print('В БД изменены данные по Этапу проекта')
            except Exception as err:
                print('Ошибка при работе с БД:', err)

    # ===============================Методы для запланированных работ===============================
    @staticmethod
    def add_new_plan_work(data):
        """ Создание новой записи в таблице Запланированные работы """
        with sqlite3.connect('templates/DB/MatrixEisenhower.db') as con:
            cur = con.cursor()
            try:
                cur.execute(''' INSERT INTO PlanWork (planned_work, date_plan,
                    time_plan, time_work_fact, id_task)
                    VALUES( ?, ?, ?, ?, ?)''', data)
                # Индекс добавленной  записи
                last = cur.lastrowid
                con.commit()
                print('В БД внесена новая запись Запланированные работы')
                return last
            except Exception as err:
                print('Ошибка при работе с БД:', err)

    @staticmethod
    def update_plan_work(data, id_work):
        """ Обновление полей запланированной работы при изменении: data= список новых значений,
            id_work= id обновляемой в таблице записи"""
        data.append(id_work)
        update_data = tuple(data)

        with sqlite3.connect('templates/DB/MatrixEisenhower.db') as con:
            cur = con.cursor()
            try:
                cur.execute(''' UPDATE PlanWork SET planned_work=?, date_plan=?,
                    time_plan=?, time_work_fact=?, id_task=?
                    WHERE id=? ''', update_data)

                con.commit()
                print(f'В БД изменены данные по Запланированной работе: {id_work}')
            except Exception as err:
                print('Ошибка при работе с БД:', err)

    @staticmethod
    def get_list_plan_works(type_task, id_plan_work=0):
        """ Запрос данных для списка плановых работ по типу,
        если type_task!=0 и id_plan_work==0 или
        данных по одной работе если  type_task==0, id_plan_work!=0"""
        with sqlite3.connect('templates/DB/MatrixEisenhower.db') as con:
            cur = con.cursor()
            if type_task != 0 and id_plan_work == 0:
                request = f''' SELECT PlanWork.*, Tasks.content_task, Tasks.type_task,
                        Tasks.date_begin, Tasks.date_end_plan, Tasks.time_plan, Tasks.time_fact,
                        Tasks.id_project, Tasks.id_stage_project,
                        COALESCE(Projects.name_project, '-'), COALESCE(StageProjects.name_stage, '-')
                        FROM PlanWork
                        INNER JOIN Tasks ON Tasks.type_task={type_task} AND PlanWork.id_task=Tasks.id
                        LEFT JOIN Projects ON Projects.id=Tasks.id_project
                        LEFT JOIN StageProjects ON StageProjects.id=Tasks.id_stage_project '''
            elif type_task == 0 and id_plan_work != 0:
                request = f''' SELECT PlanWork.*, Tasks.content_task, Tasks.type_task,
                        Tasks.date_begin, Tasks.date_end_plan, Tasks.time_plan, Tasks.time_fact,
                        Tasks.id_project, Tasks.id_stage_project,
                        COALESCE(Projects.name_project, '-'), COALESCE(StageProjects.name_stage, '-')
                        FROM PlanWork
                        INNER JOIN Tasks ON PlanWork.id={id_plan_work} AND PlanWork.id_task=Tasks.id
                        LEFT JOIN Projects ON Projects.id=Tasks.id_project
                        LEFT JOIN StageProjects ON StageProjects.id=Tasks.id_stage_project '''

            try:
                cur.execute(request)
                data = cur.fetchall()
                return data
            except Exception as err:
                print('Ошибка при работе с БД:', err)

    @staticmethod
    def get_one_plan_work(id_plan_work):
        """ Запрос данных для списка плановых работ по типу,
        если type_task!=0 и id_plan_work==0 или
        данных по одной работе если  type_task==0, id_plan_work!=0"""
        with sqlite3.connect('templates/DB/MatrixEisenhower.db') as con:
            cur = con.cursor()

            request = f''' SELECT PlanWork.*, Tasks.content_task, Tasks.type_task,
                                Tasks.date_begin, Tasks.date_end_plan, Tasks.time_plan, Tasks.time_fact,
                                Tasks.id_project, Tasks.id_stage_project, Tasks.status_stage,
                                COALESCE(Projects.name_project, '-'), COALESCE(StageProjects.name_stage, '-')
                                FROM PlanWork
                                INNER JOIN Tasks ON PlanWork.id={id_plan_work} AND PlanWork.id_task=Tasks.id
                                LEFT JOIN Projects ON Projects.id=Tasks.id_project
                                LEFT JOIN StageProjects ON StageProjects.id=Tasks.id_stage_project '''

            try:
                cur.execute(request)
                data = cur.fetchall()

                plan_work_dict = dict()

                if data:
                    # Заполняем поля в словарь
                    print(data)
                    for plan_work in data:
                        plan_work_dict = {
                            'id': plan_work[0], 'planned_work': plan_work[1],
                            'date_plan': plan_work[2], 'time_plan_work': plan_work[3], 'time_fact_work': plan_work[4],
                            'id_task': plan_work[5],
                            'content_task': plan_work[6], 'type_task': plan_work[7], 'date_begin': plan_work[8],
                            'date_end_plan': plan_work[9], 'time_plan': plan_work[10], 'time_fact': plan_work[11],
                            'id_project': plan_work[12], 'id_stage_project': plan_work[13],
                            'status_stage': plan_work[14],
                            'name_project': plan_work[15], 'name_stage': plan_work[16]}

                return plan_work_dict
            except Exception as err:
                print('Ошибка при работе с БД:', err)

    # ===============================Методы для отметок времени===============================
    @staticmethod
    def add_new_time_stamp(data):
        """ Создание новой записи в таблице Отметки времени """
        normal_data = data
        with sqlite3.connect('templates/DB/MatrixEisenhower.db') as con:
            cur = con.cursor()
            try:
                cur.execute(''' INSERT INTO TimeStamp (completed_work, date, time,
                    id_task)
                    VALUES( ?, ?, ?, ?)''', normal_data)

                con.commit()
                print('В БД внесена новая запись Отметки времени')
            except Exception as err:
                print('Ошибка при работе с БД:', err)

    @staticmethod
    def update_time_stamp(data, id_time):
        """ Обновление полей Отметки времени при изменении: data= список новых значений,
            id_time= id обновляемой в таблице записи"""
        data.append(id_time)
        update_data = tuple(data)

        with sqlite3.connect('templates/DB/MatrixEisenhower.db') as con:
            cur = con.cursor()
            try:
                cur.execute(''' UPDATE TimeStamp SET completed_work=?, date=?, time=?,
                    id_task=?
                    WHERE id=? ''', update_data)

                con.commit()
                print(f'В БД изменены данные по Отметке времени: {id_time}')
            except Exception as err:
                print('Ошибка при работе с БД:', err)

    @staticmethod
    def get_list_time_stamps(type_object, id_object):
        """ Запрос данных для списка отметок времени по типу объекта фильтрации и его ID: задача или проект """
        with sqlite3.connect('templates/DB/MatrixEisenhower.db') as con:
            cur = con.cursor()
            condition = f'Tasks.id={id_object}' if type_object == 'task' else f'Tasks.id_project={id_object}'

            request = f''' SELECT TimeStamp.*, Tasks.content_task, Tasks.type_task, Tasks.status_stage,
                        Tasks.id_project, Tasks.id_stage_project,
                        COALESCE(Projects.name_project, '-'), COALESCE(StageProjects.name_stage, '-')
                        FROM TimeStamp
                        INNER JOIN Tasks ON {condition} AND TimeStamp.id_task=Tasks.id
                        LEFT JOIN Projects ON Projects.id=Tasks.id_project
                        LEFT JOIN StageProjects ON StageProjects.id=Tasks.id_stage_project '''

            try:
                cur.execute(request)
                data = cur.fetchall()
                return data
            except Exception as err:
                print('Ошибка при работе с БД:', err)

    @staticmethod
    def get_one_time_stamp(id_time_stamp):
        """ Запрос данных для списка плановых работ по типу,
        если type_task!=0 и id_plan_work==0 или
        данных по одной работе если  type_task==0, id_plan_work!=0"""
        with sqlite3.connect('templates/DB/MatrixEisenhower.db') as con:
            cur = con.cursor()

            request = f''' SELECT TimeStamp.*, Tasks.content_task, Tasks.type_task,
                                Tasks.date_begin, Tasks.date_end_plan, Tasks.time_plan, Tasks.time_fact,
                                Tasks.id_project, Tasks.id_stage_project, Tasks.status_stage,
                                COALESCE(Projects.name_project, '-'), COALESCE(StageProjects.name_stage, '-')
                                FROM TimeStamp
                                INNER JOIN Tasks ON TimeStamp.id={id_time_stamp} AND TimeStamp.id_task=Tasks.id
                                LEFT JOIN Projects ON Projects.id=Tasks.id_project
                                LEFT JOIN StageProjects ON StageProjects.id=Tasks.id_stage_project '''

            try:
                cur.execute(request)
                data = cur.fetchall()

                time_stamps_dict = dict()

                if data:
                    # Заполняем поля в словарь
                    for time_stamp in data:
                        time_stamps_dict = {
                            'id': time_stamp[0], 'completed_work': time_stamp[1],
                            'date': time_stamp[2], 'time': time_stamp[3],
                            'id_task': time_stamp[4],
                            'content_task': time_stamp[5], 'type_task': time_stamp[6], 'date_begin': time_stamp[7],
                            'date_end_plan': time_stamp[8], 'time_plan_work': time_stamp[9],
                            'time_fact_work': time_stamp[10],
                            'id_project': time_stamp[11], 'id_stage_project': time_stamp[12],
                            'status_stage': time_stamp[13],
                            'name_project': time_stamp[14], 'name_stage': time_stamp[15]}

                return time_stamps_dict
            except Exception as err:
                print('Ошибка при работе с БД:', err)
