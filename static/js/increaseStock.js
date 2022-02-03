let numberOfRows = 1;

function validatAddItemsForm() {
    const regExp = /[a-zA-Z]/g;

    let inputs = document.getElementsByTagName('input');
    let stockInputs = document.getElementsByClassName('stockInput');
    let nameInputs = document.getElementsByClassName('nameInput');
    let inputTypes = document.getElementsByClassName('inputType');
    let itemsIntroduced = {
        'itemNames': [],
        'itemTypes': []
    };

    for (let n = 0; n < inputs.length; n++) {
        if (inputs[n].value.trim() == '') {
            alert('Do not let any field empty');
            return false;
        }
    }

    for (let n = 0; n < stockInputs.length; n++) {
        if (regExp.test(stockInputs[n].value)) {
            alert('Only numbers can be included in the field "Stock"')
            return false
        }
    }

    for (let n = 0; n < nameInputs.length; n++) {
        if (itemsIntroduced.itemNames.includes(nameInputs[n].value)) {
            index = itemsIntroduced.itemNames.indexOf(nameInputs[n].value);
            if (inputTypes[n].value == itemsIntroduced.itemTypes[index]){
                alert('You have entered the same name and the same type for two elements');
                return false;
            }    
        }
        itemsIntroduced.itemNames.push(nameInputs[n].value);
        itemsIntroduced.itemTypes.push(inputTypes[n].value);
    }
}

document.getElementById('addNewItem').addEventListener('click', function () {
    add_food = document.getElementById('WaterOrFood').textContent

    $('.formInputs').append(`
    <div class="col-md-4 rowNumber${numberOfRows}">
        <label for="nameInput" class="form-label">Name</label>
        <input type="text" class="form-control nameInput" id="nameInput" name="nameInput" autocomplete="off">
    </div>`);

    $('.formInputs').append(`
    <div class="col-md-4 rowNumber${numberOfRows}">
        <label for="stockInput" class="form-label">Stock</label>
        <input type="number" min="0" class="form-control stockInput" id="stockInput" name="stockInput" autocomplete="off">
    </div>`);

    if (add_food == 'True') {
        $('.formInputs').append(`
        <div class="col-md-4 rowNumber${numberOfRows}">
        <label for="inputType" class="form-label">Type</label>
        <select id="inputType" class="form-select inputType" name="inputType">
        <option selected>Breakfast</option>
        <option>Lunch</option>
        <option>Snack</option>
        <option>Cereal</option>
        <option>Fruit</option>
        <option>Cookie</option>
        <option>Chocolate</option>
        <option>Other</option>
        </select>
        </div>`);
    } else {
        $('.formInputs').append(`
        <div class="col-md-4 rowNumber${numberOfRows}">
        <label for="inputType" class="form-label">Tipo</label>
        <select id="inputType" class="form-select inputType" name="inputType">
        <option selected>Juice</option>
        <option>Water</option>
        <option>Soda</option>
        <option>Other</option>
        </select>
        </div>`);
    }

    numberOfRows++;
});

document.getElementById('deleteNewItem').addEventListener('click', function () {
    if (numberOfRows > 1) {
        let elem = document.getElementsByClassName(`rowNumber${numberOfRows - 1}`);        
       
        for (let n = 0; n < 3; n++){
            elem[0].remove();
        }

        numberOfRows--;
    }
});