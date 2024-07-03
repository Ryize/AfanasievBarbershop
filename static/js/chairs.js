function addChair() {
    let chair = `
    <div class="col col-12 col-lg-6 col-xxl-4 d-flex flex-column align-items-center mb-5">
                    <div class="name_chair">
                        <h3>Кресло №1</h3>
                    </div>
                    <div class="card_body">
                        <div class="card_container flex-grow-1 d-flex justify-content-center align-items-center">
                            <div class="row card_chair" id="chair">
                                <div class="col col-8 d-flex justify-content-center align-items-center">
                                    <form action="#" method="post" id="work_time">
                                        <div>
                                            <input class="input_style" type="text" id="start_time" name="start_time"
                                                value="09:00" disabled>
                                        </div>
                                        <div>
                                            <input class="input_style" type="text" id="end_time" name="end_time"
                                                value="15:00" disabled>
                                        </div>
                                        <div><input class="input_style" type="text" id="name" name="name"></div>
                                        <div>
                                            <select class="input_style" name="surname_master" id="surname_master">
                                                <option value="surname_0">Выберите мастера</option>
                                                <option value="surname_1">Кудрявцева</option>
                                                <option value="surname_2">Агафьев</option>
                                                <option value="surname_3">Поддубный</option>
                                                <option value="surname_4">Мантуров</option>
                                                <option value="surname_6">Константинопольский</option>
                                            </select>
                                        </div>
                                    </form>
                                </div>
                                <div class="col col-4 col_img_master d-flex justify-content-center align-items-center">
                                    <img class="img_master" src="img/i (2).webp" alt="Фото мастера">
                                </div>
                            </div>
                            <div class="row">
                                <button form="work_time" class="but_add_work_time"><i
                                        class="bi bi-person-fill-add"></i></button>
                            </div>
                        </div>
                        <div class="card_container flex-grow-1 d-flex justify-content-center align-items-center">
                            <div class="row card_chair">
                                <div class="col col-8 d-flex justify-content-center align-items-center">
                                    <form action="#" method="post" id="work_time">
                                        <div>
                                            <input class="input_style" type="text" id="start_time" name="start_time"
                                                value="15:00" disabled>
                                        </div>
                                        <div>
                                            <input class="input_style" type="text" id="end_time" name="end_time"
                                                value="20:00" disabled>
                                        </div>
                                        <div><input class="input_style" type="text" id="name" name="name"></div>
                                        <div>
                                            <select class="input_style" name="surname_master" id="surname_master">
                                                <option value="surname_0">Выберите мастера</option>
                                                <option value="surname_1">Кудрявцева</option>
                                                <option value="surname_2">Агафьев</option>
                                                <option value="surname_3">Поддубный</option>
                                                <option value="surname_4">Мантуров</option>
                                                <option value="surname_6">Константинопольский</option>
                                            </select>
                                        </div>
                                    </form>
                                </div>
                                <div class="col col-4 col_img_master d-flex justify-content-center align-items-center">
                                    <img class="img_master" src="img/i (2).webp" alt="Фото мастера">
                                </div>
                            </div>
                            <div class="row">
                                <button class="but_add_work_time"><i class="bi bi-person-fill-add"></i></button>
                            </div>
                        </div>
                    </div>
                </div>
    `

    let fixed_add_chair = document.getElementById("fixed_add_chair");
    fixed_add_chair.insertAdjacentHTML('beforebegin', chair);
}



window.onload = function () {
    getId('addChair').onclick = function () {
        addChair();
    };
}
// Получить элемент по id
function getId(id) {
    return document.getElementById(id);
}
