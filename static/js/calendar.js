var Cal = function (divId) {
    //Сохраняем идентификатор div
    this.divId = divId;
    // Дни недели с понедельника
    this.DaysOfWeek = [
        'Пн',
        'Вт',
        'Ср',
        'Чт',
        'Пт',
        'Сб',
        'Вс'
    ];
    // Месяцы начиная с января
    this.Months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'];
    this.MonthsAbr = ['Янв', 'Фев', 'Март', 'Апр', 'Май', 'Июнь', 'Июль', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек'];
    //Устанавливаем текущий месяц, год
    var d = new Date();
    this.currMonth = d.getMonth();
    this.currYear = d.getFullYear();
    this.currDay = d.getDate();
};
// Переход к следующему месяцу
Cal.prototype.nextMonth = function () {
    if (this.currMonth == 11) {
        this.currMonth = 0;
        this.currYear = this.currYear + 1;
    }
    else {
        this.currMonth = this.currMonth + 1;
    }
    this.showcurr();
    this.showAbrMonth();
};
// Переход к предыдущему месяцу
Cal.prototype.previousMonth = function () {
    if (this.currMonth == 0) {
        this.currMonth = 11;
        this.currYear = this.currYear - 1;
    }
    else {
        this.currMonth = this.currMonth - 1;
    }
    this.showcurr();
    this.showAbrMonth();
};
// Показать текущий месяц
Cal.prototype.showcurr = function () {
    this.showMonth(this.currYear, this.currMonth);
};

Cal.prototype.showAbrMonth = function () {

    let arrow_l = '<i class="bi bi-arrow-left-square-fill arrow_l"></i>'
    let arrow_r = '<i class="bi bi-arrow-right-square-fill arrow_r"></i>'

    let prev_btn = arrow_l;
    let next_btn = '';

    if (this.currMonth == 11) {
        prev_btn += this.MonthsAbr[this.currMonth - 1];
        next_btn += this.MonthsAbr[0] + arrow_r;
    }
    else if (this.currMonth == 0) {
        prev_btn += this.MonthsAbr[11];
        next_btn += this.MonthsAbr[this.currMonth + 1] + arrow_r;
    }
    else {
        prev_btn += this.MonthsAbr[this.currMonth - 1];
        next_btn += this.MonthsAbr[this.currMonth + 1] + arrow_r;
    }

    document.getElementById('btnPrev').innerHTML = prev_btn
    document.getElementById('btnNext').innerHTML = next_btn
};

// Показать месяц (год, месяц)
Cal.prototype.showMonth = function (y, m) {
    var d = new Date()
        // Первый день недели в выбранном месяце
        , firstDayOfMonth = new Date(y, m, 7).getDay()
        // Последний день выбранного месяца
        , lastDateOfMonth = new Date(y, m + 1, 0).getDate()
        // Последний день предыдущего месяца
        , lastDayOfLastMonth = new Date(y, m, 0).getDate();
    var html = '<table>';
    // Запись выбранного месяца и года
    html += '<thead><tr>';
    html += '<td colspan="7">' + this.Months[m] + ' ' + y + '</td>';
    html += '</tr></thead>';
    // заголовок дней недели
    html += '<tr class="week_days">';
    for (var i = 0; i < this.DaysOfWeek.length; i++) {
        html += '<td>' + this.DaysOfWeek[i] + '</td>';
    }
    html += '</tr>';
    // Записываем дни
    var i = 1;
    do {
        var dow = new Date(y, m, i).getDay();
        // Начать новую строку в понедельник
        if (dow == 1) {
            html += '<tr>';
        }
        // Если первый день недели не понедельник показать последние дни предыдущего месяца
        else if (i == 1) {
            html += '<tr>';
            var k = lastDayOfLastMonth - firstDayOfMonth + 1;
            for (var j = 0; j < firstDayOfMonth; j++) {
                html += '<td class="not-current">' + k + '</td>';
                k++;
            }
        }
        // Записываем текущий день в цикл
        var chk = new Date();
        var chkY = chk.getFullYear();
        var chkM = chk.getMonth();
        if (chkY == this.currYear && chkM == this.currMonth && i == this.currDay) {
            if (dow == 0 || dow == 6) {
                html += '<td class="today weekend"><a href="#" class="calendar-date" data-date="' + y + '-' + (m + 1) + '-' + i + '">' + i + '</a></td>';
            }
            else {
                html += '<td class="today"><a href="#" class="calendar-date" data-date="' + y + '-' + (m + 1) + '-' + i + '">' + i + '</a></td>';
            }
        } else {
            if (dow == 0 || dow == 6) {
                html += '<td class="normal weekend"><a href="#" class="calendar-date" data-date="' + y + '-' + (m + 1) + '-' + i + '">' + i + '</a></td>';
            }
            else {
                html += '<td class="normal"><a href="#" class="calendar-date" data-date="' + y + '-' + (m + 1) + '-' + i + '">' + i + '</a></td>';
            }
        }
        // закрыть строку в воскресенье
        if (dow == 0) {
            html += '</tr>';
        }
        // Если последний день месяца не воскресенье, показать первые дни следующего месяца
        else if (i == lastDateOfMonth) {
            var k = 1;
            for (dow; dow < 7; dow++) {
                html += '<td class="not-current">' + k + '</td>';
                k++;
            }
        }
        i++;
    } while (i <= lastDateOfMonth);
    // Конец таблицы
    html += '</table>';
    // Записываем HTML в div
    document.getElementById(this.divId).innerHTML = html;

    this.addDateClickHandlers();
};

Cal.prototype.addDateClickHandlers = function () {
    const dates = document.querySelectorAll('.calendar-date');
    const branchSelect = document.getElementById('branchSelect');

    dates.forEach(date => {
        date.addEventListener('click', function (event) {
            event.preventDefault();
            const selectedDate = this.getAttribute('data-date');
            const selectedBranch = branchSelect.value;

            if (selectedBranch) {
                const url = `/masters/schedule/${selectedBranch}/${selectedDate}/`;
                window.location.href = url;
            } else {
                alert('Please select a branch first.');
            }
        });
    });
};

// При загрузке окна
window.onload = function () {
    // Начать календарь
    var c = new Cal("divCal");
    c.showcurr();
    c.showAbrMonth();
    // Привязываем кнопки «Следующий» и «Предыдущий»
    getId('btnNext').onclick = function () {
        c.nextMonth();
    };
    getId('btnPrev').onclick = function () {
        c.previousMonth();
    };
}
// Получить элемент по id
function getId(id) {
    return document.getElementById(id);
}
