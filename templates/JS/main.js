//**************** Общие методы *********************************
// Извлечение текущей даты в формате для форм
function getToday() {
    var today = new Date();
    console.log(today)
    var dd = today.getDate();
    if (dd <10) {
        dd = '0' + dd;
    }
    var mm = today.getMonth()+1; //January is 0!
    if (mm < 10) {
        mm = '0' + mm;
    }
    var yyyy = today.getFullYear();
    today = yyyy + '-' + mm + '-' + dd;

    return today
}

// Запаковка списка параметров в строку
function packParameters(fields) {
  var list_parameters = '';
  var index;
  for (index = 0; index < fields.length; ++index) {
      if (index != fields.length - 1) {
          list_parameters += fields[index] + '||*||';
      }
      else {
          list_parameters += fields[index];
      }
  }
  console.info('Параметры после склейки: ' + list_parameters)
  return list_parameters
}

// POST AJAX запрос на сервер
function newPOST_AJAXRequest(func, list_parameters, change_block) {
    var xhr = new XMLHttpRequest();


    list_parameters = encodeURIComponent(list_parameters)

    xhr.open('POST', func, true);
    xhr.onreadystatechange = function() {
        // onreadystatechange активируется при получении ответа сервера
        if (xhr.readyState == 4) return
        clearTimeout(xhrTimeout) // очистить таймаут при наступлении readyState 4
        if (xhr.status == 200) {
                if (change_block)
                    change_block.innerHTML = xhr.responseText;
        }
        else alert('Запрос завершился неудачно ' + xhr.status)
    }
    xhr.send(list_parameters);

    var xhrTimeout = setTimeout(function () {
    xhr.abort()
    handleError('Timeout')
    }, 10000)
}

// Сообщение об отсутствии ответа с сервера
function handleError(eventType) {
    if (eventType == 'Timeout')
      alert('Связь прервана произошла ошибка')

}

// GET AJAX запрос на сервер
function newAJAXRequest(func, list_parameters, change_block) {
    var xhr = new XMLHttpRequest();
    list_parameters = encodeURIComponent(list_parameters)

    xhr.open('GET', func + '?'+ list_parameters, true);
    xhr.onreadystatechange = function() {
        // onreadystatechange активируется при получении ответа сервера
        if (xhr.readyState == 4) return
        clearTimeout(xhrTimeout) // очистить таймаут при наступлении readyState 4
        if (xhr.status == 200) {
                if (change_block)
                    change_block.innerHTML = xhr.responseText;
        }
        else {console.log('Запрос завершился неудачно ' + xhr.status)}
    }

    xhr.send();
    var xhrTimeout = setTimeout(function () {
    xhr.abort()
    handleError('Timeout')
    }, 10000)

}

// Закрытие мини формы
function close_mini_form() {
  let task = document.getElementById('panel_mini_form');
  task.style.display="none";
  document.body.style.overflow = 'visible';
  task.innerHTML = "";
}

// Открытие мини формы
function open_mini_form() {
  let task = document.getElementById('panel_mini_form');
  console.log('task: ' + task)
  task.style.display="initial";
  document.body.style.overflow = 'hidden';
  console.info('Мини-форма открыта')
}


//**************** ПРОЕКТЫ *****************************
// Сохранение нового проекта и изменение существующего
function saveUpdateProject(id_project=0, status_new=0) {
  // Поля диалога проекта
  // Краткое наименование проекта
  let name_project = document.getElementById('name_project');
  // Дата начала выполнения проекта
  let date_begin = document.getElementById('date_begin');
  // Плинируемая дата выполнения проекта
  let date_end_plan = document.getElementById('date_end_plan');
  // Планируемое время на выполнение проекта
  let time_plan = document.getElementById('time_plan');

  // Содержание проекта
  let content_project = document.getElementById('content_task');

  // Фактическая дата завершения проекта
  let date_end_fact = document.getElementById('date_end_fact');
  // Фактически затраченное время на выполнение проекта
  let time_spent = document.getElementById('time_spent');
  // Комментарий о выпонении
  let execution_comment = document.getElementById('execution_comment');
  // Статус проекта(0 - новыя, 1 - в работе, 2 - завершена, 3 - отклонена)
  let status_project = document.getElementById('status_project');
  // Валидация данных
  var beginValue = date_begin.value.split('-');
  var planValue = date_end_plan.value.split('-');
  var factValue = date_end_fact.value.split('-');

  var beginDate = new Date (beginValue [0], (beginValue [1] - 1 ), beginValue [2]);
  var planDate = new Date (planValue [0], (planValue [1] - 1 ), planValue [2]);
  var factDate = new Date (factValue [0], (factValue [1] - 1 ), factValue [2]);

  if (name_project.value == '') {
    alert('Введите наименование проекта')
  }
  else if (time_plan.value <= 0) {
    alert('Запланированное на проект время должно быть  меньше или равно 0 часов')
  }
  else if (date_begin.value == '') {
    alert('Введите дату начала проекта')
  }
  else if (date_end_plan.value == '') {
    alert('Введите окончания начала проекта')
  }
  else if (beginDate > planDate) {
    alert('Дата начала проекта не может быть позже даты окончания проекта')
  }
  else if (content_project.value == '') {
    alert('Введите содержание проекта')
  }
  else {
    // Создание нового проекта
    if (id_project == 0) {
        var fields = [name_project.value, content_project.value, date_begin.value,
          date_end_plan.value, date_end_fact.value, time_plan.value,
          time_spent.value, execution_comment.value, 1]
        console.log(fields)

        var list_parameters = packParameters(fields);

        console.log(list_parameters);
        var block_list_project = document.getElementById('main_panel');
        newPOST_AJAXRequest('CreateProject', list_parameters, block_list_project)
    }
    // Обновление сохраненного проекта
    else {
        var fields
        // просто обновляем проект
        if (status_new == 0) {
          fields = [id_project, name_project.value, content_project.value, date_begin.value,
          date_end_plan.value, date_end_fact.value, time_plan.value,
          time_spent.value, execution_comment.value, status_project.value]
        }
        // Завершаем или отменяем проект
        else if (status_new == 2 || status_new == 3) {
          var d_fact = date_end_fact.value
          if (!date_end_fact.value) {
            d_fact = getToday()
          }

          fields = [id_project, name_project.value, content_project.value, date_begin.value,
          date_end_plan.value, d_fact, time_plan.value,
          time_spent.value, execution_comment.value, status_new]
        }

        var list_parameters = packParameters(fields);

        var block_list_project = document.getElementById('main_panel');
        newPOST_AJAXRequest('UpdateProject', list_parameters, block_list_project)
    }
  }
}

// Открытие формы создания нового проекта
function openProjectForm(id_project=0) {
  var change_block_page = document.getElementById('main_panel');
  if (change_block_page) {
    newAJAXRequest('OpenProjectForm', id_project, change_block_page)
  }
}

// Закрытие формы проекта
function closeProject() {
  var change_block_page = document.getElementById('main_panel');
  if (change_block_page) {
    newAJAXRequest('CloseProject', 0, change_block_page)
  }
}

// Фильтрация пректов в реестре по статусу
function changeFilterProjects() {
  var value_filter = document.getElementById('select_filter_status_projects').value;
  var change_block_page = document.getElementById('list_project');
  if (change_block_page) {
    newAJAXRequest('ChangeFilterProjects', value_filter, change_block_page)
  }
}

// Удаление проекта
function deleteProject(id_project) {
  var response = confirm('Удалить проект?');
  if (response) {
     var change_block_page = document.getElementById('main_panel');
     newAJAXRequest('DeleteProject', id_project, change_block_page)
  }
}

//**************** ЗАДАЧИ *****************************
// Открытие сохраненной задачи
function openTaskForm(id_task) {
  var change_block_page = document.getElementById('main_panel');
  var block_page = document.getElementById('field_form_task');
  if (block_page && change_block_page) {
    newAJAXRequest('OpenTaskForm', id_task, change_block_page)
  }
  else {
    change_block_page = document.documentElement;
    newAJAXRequest('OpenTaskForm', id_task, change_block_page)
  }
}

// Обновление карточки задачи при изменении затраченного времени по ней
function updateTaskForm(id_task) {
  var change_task = document.getElementById('task_form' + id_task);
  if (change_task) {
    openTaskForm(id_task);
  }
}

// Обновление одной карточки задачи в реестре после изменений
function updateTaskCard(id_task) {
  var change_block_page = document.getElementById('task' + id_task);
  if (change_block_page) {
    newAJAXRequest('UpdateTaskCard', id_task, change_block_page);
  }
}

// Сохранение новой задачи и обновление существующей
function newTaskRequest(id_task, status = 1) {
  // Поля диалога задачи
  // Тип задачи(A-1, B-2, C-3, D-4)
  let type_task = document.getElementById('select_type');
  // Связанный проект(0 - нет связи)
  let id_project = document.getElementById('select_project');
  // Связанный этап проекта(0 - нет связи)
  let id_stage_project = document.getElementById('select_stage_project');

  // Дата начала выполнения задачи
  let date_begin = document.getElementById('date_begin');
  // Плинируемая дата выполнения задачи
  let date_end_plan = document.getElementById('date_end_plan');
  // Планируемое время на выполнение задачи
  let time_plan = document.getElementById('time_plan');

  // Содержание задачи
  let content_task = document.getElementById('content_task');

  // Фактическая дата завершения задачи
  let date_end_fact = document.getElementById('date_end_fact');
  // Фактически затраченное время на выполнение задачи
  let time_spent = document.getElementById('time_spent');
  // Комментарий о выпонении
  let execution_comment = document.getElementById('execution_comment');
  // Статус задачи(0 - новыя, 1 - в работе, 2 - завершена, 3 - отклонена)
  let status_task = document.getElementById('status_task');
  // Валидация данных
  var beginValue = date_begin.value.split('-');
  var planValue = date_end_plan.value.split('-');
  var factValue = date_end_fact.value.split('-');

  var beginDate = new Date (beginValue [0], (beginValue [1] - 1 ), beginValue [2]);
  var planDate = new Date (planValue [0], (planValue [1] - 1 ), planValue [2]);
  var factDate = new Date (factValue [0], (factValue [1] - 1 ), factValue [2]);


  if (time_plan.value <= 0 || content_task.value == '') {
    alert('Не заполнены обязательные поля: содержание задачи и плановое время должно быть больше 0 \n задача не сохранена');
    return;
  }

  var date_end_fact_save = date_end_fact.value

  if (status == 1) {
    if (status_task.value == 0) {
      status = 1;
    }
    else {
      status = status_task.value;
    }
  }
  else {
    if (status_task.value == 0) {
       alert('Завершить или отменить задачу нельзя: задача не сохранена');
       return;
    }
    if (!date_end_fact.value) {
      date_end_fact_save = getToday()
    }
  }

  var fields = [content_task.value, type_task.value, date_begin.value,
      date_end_plan.value, date_end_fact_save, time_plan.value,
      time_spent.value, execution_comment.value,
      id_project.value, id_stage_project.value,  status]

  if (id_task != 0) {
    fields.unshift(id_task);
  }

  var list_parameters = packParameters(fields)

  if (id_task == 0) {

      var change_block_page = document.getElementById('insert_task');
      if (change_block_page) {
        change_block_page.id = 'insert_task33';
        newPOST_AJAXRequest('CreateTask', list_parameters, change_block_page)
      }
      else {
          var block_list_task = document.getElementById('list_tasks');
          newPOST_AJAXRequest('CreateTask', list_parameters, block_list_task)
      }
      openTaskForm(0)
  }
  else {
     var change_block_page = document.getElementById('main_panel');
     var task_in_registry = document.getElementById('task' + id_task);
     if (task_in_registry) {
        // Обновление карточки изменяемой задачи в реестре
     }
     newPOST_AJAXRequest('UpdateTask', list_parameters, change_block_page)
     updateTaskCard(id_task)
  }
}

// Удаление задач
function deleteTask(id_task) {
    if (id_task == 0) {
        alert('Удаление невозможно: задача не сохранена');
    }
    else {
        var response = confirm('Удалить задачу?');
        if (response) {
            // Фактически затраченное время на выполнение задачи
            let time_spent = document.getElementById('time_spent');
            if (time_spent > 0) {
                alert('Нельзя удалить задачу, на неё было потрачено время\n Удалите отметки времени к задаче или отмените задачу')
            }
            else {
                var block_list_task = document.getElementById('main_panel');
                newAJAXRequest('DeleteTask', id_task, block_list_task)
                var task_in_registry = document.getElementById('task' + id_task);
                if (task_in_registry) {
                    task_in_registry.remove()
                }
            }
        }
    }
}

// Фильтрация реестра задач по статусу
function changeFilterTask(change_filter) {
  var value_filter
  if (change_filter == 'task') {
    // Установленное значение фильтра задач
    value_filter = document.getElementById('select_filter_task').value;
  }
  else {
    // Установленное значение фильтра проектов
    value_filter = document.getElementById('select_filter_project').value;
  }
  var fields = [change_filter, value_filter];
  var list_parameters = packParameters(fields);

  var change_block_page = document.getElementById('list_tasks');
  if (change_block_page) {
    newAJAXRequest('ChangeFilterTask', list_parameters, change_block_page)
  }

}

// Изменение цвета блоков задачи при изменении её типа
function changeTypeTack() {
    // Изменение цвета заголовка задачи
    // Тип задачи(A-1, B-2, C-3, D-4)
    let type_task = document.getElementById('select_type');
    // Блоки цветовой подсветки типа задачи
    let header_task = document.getElementById('header_task');
    let block_type = document.getElementById('block_type');
    let block_datetime = document.getElementById('block_datetime');
    let block_content_task = document.getElementById('block_content_task');
    let block_fact = document.getElementById('block_fact');
    let block_fact2 = document.getElementById('block_fact2');

    var color = ''
    if (type_task.value == 1)
        color = 'rgba(227, 2, 6, 0.2)';
    else if (type_task.value == 2)
        color = 'rgba(12, 196, 24, 0.2)';
    else if (type_task.value == 3)
        color = 'rgba(227, 141, 2, 0.3)';
    else if (type_task.value == 4)
        color = 'rgba(227, 2, 208, 0.3)';

    header_task.style.backgroundColor = color;
    block_type.style.backgroundColor = color;
    block_datetime.style.backgroundColor = color;
    block_content_task.style.backgroundColor = color;
    block_fact.style.backgroundColor = color;
    block_fact2.style.backgroundColor = color;
}

// Установка дефолтных значений в поля задачи
function defaultFieldTask() {
    // Поля диалога задачи
    // Тип задачи(A-1, B-2, C-3, D-4)
    let type_task = document.getElementById('select_type');
    // Связанный проект(0 - нет связи)
    let id_project = document.getElementById('select_project');
    // Связанный этап проекта(0 - нет связи)
    let id_stage_project = document.getElementById('select_stage_project');

    // Дата начала выполнения задачи
    let date_begin = document.getElementById('date_begin');
    // Плинируемая дата выполнения задачи
    let date_end_plan = document.getElementById('date_end_plan');
    // Планируемое время на выполнение задачи
    let time_plan = document.getElementById('time_plan');

    // Содержание задачи
    let content_task = document.getElementById('content_task');

    // Фактическая дата завершения задачи
    let date_end_fact = document.getElementById('date_end_fact');
    // Фактически затраченное время на выполнение задачи
    let time_spent = document.getElementById('time_spent');
    // Комментарий о выпонении
    let execution_comment = document.getElementById('execution_comment');
    // Статус задачи(0 - новыя, 1 - в работе, 2 - завершена, 3 - отклонена)
    let status_task = document.getElementById('status_task');
    // Устанавливаем цвет блоков согласно типу задачи
    content_task.value = '';
    type_task.value = 1;
    date_begin.value =  getToday();
    date_end_plan.value =  getToday();
    date_end_fact.value = '';
    time_plan.value = 1;
    time_spent.value = 0;
    execution_comment.value = '';
    id_project.value = 0;
    id_stage_project.value = 0;
    status_task.value = 0;

    changeTypeTack();
}


//**************** ПЛАНОВЫЕ РАБОТЫ *****************************
// Открытие мини-формы новой плановой работы
function openNewPlanWorkForm(id_task) {
  if (id_task == 0) {
     alert('Запланировать работу нельзя: задача не сохранена');
  }
  else {
    var change_block_page = document.getElementById('panel_mini_form');
    newAJAXRequest('OpenNewPlanWorkForm', id_task, change_block_page)
    open_mini_form()
  }
}

// Открытие формы сохраненной плановой работы
function openPlanWorkForm(id_plan_work) {
  var change_block_page = document.getElementById('panel_mini_form');
  newAJAXRequest('OpenPlanWorkForm', id_plan_work, change_block_page)
  open_mini_form()
}

// Сохранение новой плановой работы по задаче
function saveNewPlanWorkForm(id_task, type_task) {
  // Поля даилога мини-формы
  // Поле даты мини-формы
  var date_input_form = document.getElementById('date_input_form');
  // Поле времени мини-формы
  var time_input_form = document.getElementById('time_plan_input_form');
  // Поле комментария мини-формы
  var content_input_form = document.getElementById('content_input_form');

  var dateValue = date_input_form.value.split('-');
  var dateValue = new Date (dateValue [0], (dateValue [1] - 1 ), dateValue [2]);

  var fields = [content_input_form.value, date_input_form.value,
      time_input_form.value, 0, id_task]

  var list_parameters = packParameters(fields);

  var id_object = 'insert_plan_work' + type_task;
  var change_block_page = document.getElementById(id_object);
  if (change_block_page) {
    change_block_page.id = 'insert_plan_work33';
    newPOST_AJAXRequest('SaveNewPlanWorkForm', list_parameters, change_block_page);
    close_mini_form();
  }
  else {
    var id_block = '';
    if (type_task == 1)
      id_block = 'urgent-important';
    else if (type_task == 2)
      id_block = 'non-urgent-important';
    else if (type_task == 3)
      id_block = 'urgent-unimportant';
    else if (type_task == 4)
      id_block = 'non-urgent-unimportant';
    change_block_page =  document.getElementById(id_block);
    newPOST_AJAXRequest('SaveNewPlanWorkForm', list_parameters, change_block_page);
    close_mini_form();
  }
}

// Внесение изменений в сохраненную плановую работу
function updatePlanWork(id_plan_work, time_work_fact, id_task) {
  // Поле даты мини-формы
  var date_input_form = document.getElementById('date_input_form');
  // Поле времени мини-формы
  var time_input_form = document.getElementById('time_plan_input_form');
  // Поле комментария мини-формы
  var content_input_form = document.getElementById('content_input_form');

  var dateValue = date_input_form.value.split('-');
  var dateValue = new Date (dateValue [0], (dateValue [1] - 1 ), dateValue [2]);

  var fields = [id_plan_work, content_input_form.value, date_input_form.value,
      time_input_form.value, time_work_fact, id_task]

  var list_parameters = packParameters(fields);

  var id_object = 'plan_work' + id_plan_work;
  var change_block_page = document.getElementById(id_object);
  if (change_block_page) {
    newPOST_AJAXRequest('UpdatePlanWorkForm', list_parameters, change_block_page);
    close_mini_form();
  }
}

// Завершение плановой работы
function do_execution_plan_work(id_task, id_plan_work) {
  var response = confirm('Завершить плановую работу?');
  if (response) {
    var response2 = confirm('Отметить время по связанной задаче?');
    if (response2) {
      deletePlanWork(id_plan_work)
      openNewTimeStampForm(id_task)
    }
    else {
      deletePlanWork(id_plan_work)
    }
  }
}

// Удаление плановой работы из матрицы Эйзенхауэра в предварительным вопросом
function deletePlanWorkFromRegistry(id_plan_work) {
  var response = confirm('Отменить плановую работу?');
  if (response) {
    deletePlanWork(id_plan_work)
  }
}

// Удаление плановой работы из матрицы Эйзенхауэра
function deletePlanWork(id_plan_work) {
  close_mini_form()
  // Поле даты мини-формы
  var id_block = id_plan_work;

  id_block = 'plan_work' + id_plan_work;

  var change_block_page = document.getElementById(id_block);

  if (change_block_page.classList.contains('plan_work_card')) {
    change_block_page.classList.remove('plan_work_card');
  }

    newAJAXRequest('DeletePlanWorkFromRegistry', id_plan_work, change_block_page);
}


//**************** ОТМЕТКИ ВРЕМЕНИ *****************************
// Открытие мини-формы новой отметки времени
function openNewTimeStampForm(id_task) {
  if (id_task == 0) {
     alert('Отметить время нельзя: задача не сохранена');
  }
  else {
    var change_block_page = document.getElementById('panel_mini_form');
    newAJAXRequest('OpenNewTimeStampForm', id_task, change_block_page)
    open_mini_form()
  }
}

// Открытие мини-формы сохраненной отметки времени
function openTimeStampForm(id_time_stamp) {
    var change_block_page = document.getElementById('panel_mini_form');
    newAJAXRequest('OpenTimeStampForm', id_time_stamp, change_block_page)
    open_mini_form()
}

// Установка отметки времени по плановой работе
function do_time_stamp_for_plan_work(id_task) {
  close_mini_form();
  openNewTimeStampForm(id_task)
}

// Сохранение новой отметки времени по задаче
function saveNewTimeStampForm(id_task) {
  // Поля даилога мини-формы
  // Поле даты мини-формы
  var date_input_form = document.getElementById('date_input_form');
  // Поле времени мини-формы
  var time_input_form = document.getElementById('time_input_form');
  // Поле комментария мини-формы
  var content_input_form = document.getElementById('content_input_form');

  var dateValue = date_input_form.value.split('-');
  var dateValue = new Date (dateValue [0], (dateValue [1] - 1 ), dateValue [2]);

  var fields = [content_input_form.value, date_input_form.value,
      time_input_form.value, id_task]

  var list_parameters = packParameters(fields);

  newPOST_AJAXRequest('SaveNewTimeStampForm', list_parameters);
  updateTaskCard(id_task)
  close_mini_form();

  // Обновление формы задачи, если она открыта
  updateTaskForm(id_task)
}

// Обновление сохраненной отметки времени
function updateTimeStamp(id_time_stamp, id_task) {
  // Поля даилога мини-формы
  // Поле даты мини-формы
  var date_input_form = document.getElementById('date_input_form');
  // Поле времени мини-формы
  var time_input_form = document.getElementById('time_input_form');
  // Поле комментария мини-формы
  var content_input_form = document.getElementById('content_input_form');

  var dateValue = date_input_form.value.split('-');
  var dateValue = new Date (dateValue [0], (dateValue [1] - 1 ), dateValue [2]);

  var fields = [id_time_stamp, content_input_form.value, date_input_form.value,
      time_input_form.value, id_task]

  var list_parameters = packParameters(fields);

  var change_block_page = document.getElementById('time_stamp' + id_time_stamp);
  newPOST_AJAXRequest('UpdateTimeStamp', list_parameters, change_block_page);
  close_mini_form();

  // Обновление формы задачи, если она открыта
  updateTaskForm(id_task)
}

// Отрисовка списка отметок времени в правой панели по задаче или проекту
function drawListTimeStamp(type_object, id_object) {
  var change_block_page = document.getElementById('right_panel');
  var param = packParameters([type_object, id_object])
  // Статус задачи(0 - новыя, 1 - в работе, 2 - завершена, 3 - отклонена)
  let status_task = document.getElementById('status_task');

  if (id_object == 0) {
    alert('Построить реестр отметок времени нельзя: задача не сохранена');
    return;
  }
  else {
    if (change_block_page) {
      newAJAXRequest('DrawListTimeStamp', param, change_block_page)
    }
  }
}

// Закрытие реестра с отметками времени
function closeListTimeStamps() {
var change_block_page = document.getElementById('right_panel');
if (change_block_page) {
      newAJAXRequest('CloseListTimeStamps', 0, change_block_page)
    }
}

// Удаление отметки времени
function deleteTimeStamp(id_time_stamp) {
  var response = confirm('Удалить отметку времени?');
  if (response) {
      newAJAXRequest('DeleteTimeStamp', id_time_stamp)
      var time_stamp_in_registry = document.getElementById('time_stamp' + id_time_stamp);
      if (time_stamp_in_registry) {
        time_stamp_in_registry.remove()
      }
      close_mini_form()
  }
}
