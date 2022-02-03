// variables necessaries for one specific date filter
let totalInitialFoodInStock = 0;
let totalFinalFoodInStock = 0;
let totalInitialBeveragesInStock = 0;
let totalFinalBeveragesInStock = 0;

// variables necessaries for between dates filter

let averageFoodInStockPerDay = 0; // query the selector the data is provided by the server
let averageBeveragesdInStockPerDay = 0;
let averageFoodExpensesPerDay = 0;
let averageBeveragesExpensesPerDay = 0;

// variables necessaries for both
let totalFoodConsumed = 0;
let totalBeveragesConsumed = 0;
let totalFoodAdded = 0;
let totalBeveragesAdded = 0;

// getting the rows 
const breakfasts = document.querySelectorAll('.breakfastRow');
const lunch = document.querySelectorAll('.lunchRow');
const snacks = document.querySelectorAll('.snackRow');
const cereals = document.querySelectorAll('.cerealRow');
const fruits = document.querySelectorAll('.fruitRow');
const cookies = document.querySelectorAll('.cookieRow');
const chocolates = document.querySelectorAll('.chocolateRow');
const otherFoods = document.querySelectorAll('.otherFoodRow');

const waters = document.querySelectorAll('.waterRow');
const sodas = document.querySelectorAll('.sodaRow');
const juices = document.querySelectorAll('.juiceRow');
const othersBeverages = document.querySelectorAll('.otherBeverageRow');

let showBreakfasts = true;
let showLunch = true;
let showSnacks = true;
let showCereals = true;
let showFruits = true;
let showCookies = true;
let showChocolates = true;
let showOtherFoods = true;

let showWaters = true;
let showJuices = true;
let showSodas = true;
let showOtherBeverages = true;

// storing the rows in a js object table
const items = {
    'breakfast': breakfasts,
    'lunch': lunch,
    'snacks': snacks,
    'cereals': cereals,
    'fruits': fruits,
    'cookies': cookies,
    'chocolates': chocolates,
    'otherFoods': otherFoods,
    'waters': waters,
    'sodas': sodas,
    'juices': juices,
    'otherBeverages': othersBeverages,
};

let nameOfFoodItems = ['breakfast', 'lunch', 'snacks', 'cereals', 'fruits', 'cookies', 'chocolates', 'otherFoods'];
let nameOfBeveragesItems = ['waters', 'sodas', 'juices', 'otherBeverages'];
let foodItemsToShowArray = [showBreakfasts, showLunch, showSnacks, showCereals, showFruits];
let beverageItemsToShowArray = [showWaters, showJuices, showSodas, showOtherBeverages];


// Checking if the worked days is in avaliable that will mean what the filters must work between dates
document.querySelectorAll('.filter').forEach(item => {
    if (document.getElementById('workedDays') != null) {
        days = document.getElementById('workedDays').textContent;
        betweenDates = true;
    } else {
        betweenDates = false;
    }

    // managing the click events
    // depending on the id the filter have to evaluate some values and show others 
    item.addEventListener('click', event => {
        let itemToEvaluate = null
        if (item.id == 'showBreakfasts') {
            breakfasts.forEach(i => {
                adding = !i.classList.toggle('invisible');
            })
            itemToEvaluate = 'breakfast';
            showBreakfasts = adding;

        } else if (item.id == 'showLunch') {
            lunch.forEach(i => {
                adding = !i.classList.toggle('invisible');
            })
            showLunch = adding;
            itemToEvaluate = 'lunch';

        } else if (item.id == 'showSnacks') {
            snacks.forEach(i => {
                adding = !i.classList.toggle('invisible');
            })
            showSnacks = adding;
            itemToEvaluate = 'snacks';

        } else if (item.id == 'showCereals') {
            cereals.forEach(i => {
                adding = !i.classList.toggle('invisible');
            })
            showCereals = adding;
            itemToEvaluate = 'cereals';

        } else if (item.id == 'showFruits') {
            fruits.forEach(i => {
                adding = !i.classList.toggle('invisible');
            })
            showFruits = adding;
            itemToEvaluate = 'fruits';

        } else if (item.id == 'showCookies') {
            cookies.forEach(i => {
                adding = !i.classList.toggle('invisible');
            })
            showCookies = adding;
            itemToEvaluate = 'cookies';

        } else if (item.id == 'showChocolates') {
            chocolates.forEach(i => {
                adding = !i.classList.toggle('invisible');
            })
            showChocolates = adding;
            itemToEvaluate = 'chocolates';

        } else if (item.id == 'showOtherFoods') {
            otherFoods.forEach(i => {
                adding = !i.classList.toggle('invisible');
            })
            showOtherFoods = adding;
            itemToEvaluate = 'otherFoods';

        }

        foodItemsToShowArray = [showBreakfasts, showLunch, showSnacks, showCereals, showFruits, showCookies, showChocolates, showOtherFoods];

        if (betweenDates && itemToEvaluate) {
            getAverageOfItemsConsumption(food = true, beverages = true, days = days)
            return;
        } else if (itemToEvaluate && !betweenDates) {
            getStocks(food = true, beverages = false, adding = adding, itemToEvaluate = itemToEvaluate);
            return;
        }

        // for beverages
        if (item.id == 'showWaters') {
            waters.forEach(i => {
                adding = !i.classList.toggle('invisible');
            })
            showWaters = adding;
            itemToEvaluate = 'waters';

        } else if (item.id == 'showSodas') {
            sodas.forEach(i => {
                adding = !i.classList.toggle('invisible');
            })
            showSodas = adding;
            itemToEvaluate = 'sodas';

        } else if (item.id == 'showJuices') {
            juices.forEach(i => {
                adding = !i.classList.toggle('invisible');
            })
            showJuices = adding;
            itemToEvaluate = 'juices';

        } else if (item.id == 'showOtherBeverages') {
            othersBeverages.forEach(i => {
                adding = !i.classList.toggle('invisible');
            })
            showOtherBeverages = adding;
            itemToEvaluate = 'otherBeverages';
        }
        beverageItemsToShowArray = [showWaters, showJuices, showSodas, showOtherBeverages];
        if (betweenDates) {
            getAverageOfItemsConsumption(food = false, beverages = true, days = days);
            return;
        } else {
            getStocks(food = false, beverages = true, adding = adding, itemToEvaluate = itemToEvaluate);
            return;
        }
    });
});


function getStocks(food = false, beverages = false, adding = false, itemToEvaluate) {
    //Get food initital stock
    if (itemToEvaluate === 'all') {
        let initialStock = 0;
        let finalStock = 0;
        let consumption = 0;
        let added = 0;
        nameOfFoodItems.forEach(name => {
            items[name].forEach(item => {

                initialStock += parseInt(item.querySelector('.initialStock').textContent);
                finalStock += parseInt(item.querySelector('.finalStock').textContent);
                consumption += parseInt(item.querySelector('.consumption').textContent);
                added += parseInt(item.querySelector('.added').textContent);

            });
        });

        totalInitialFoodInStock = initialStock;
        totalFinalFoodInStock = finalStock;
        totalFoodConsumed = consumption;
        totalFoodAdded = added;

        document.getElementById('initialFoodStock').textContent = initialStock;
        document.getElementById('finalFoodStock').textContent = finalStock;
        document.getElementById('totalFoodConsumption').textContent = consumption;
        document.getElementById('totalFoodAdded').textContent = added;

        initialStock = 0;
        finalStock = 0;
        consumption = 0;
        added = 0;
        nameOfBeveragesItems.forEach(name => {
            items[name].forEach(item => {
                initialStock += parseInt(item.querySelector('.initialStock').textContent);
                finalStock += parseInt(item.querySelector('.finalStock').textContent);
                consumption += parseInt(item.querySelector('.consumption').textContent);
                added += parseInt(item.querySelector('.added').textContent);
            });
        });

        totalInitialBeveragesInStock = initialStock;
        totalFinalBeveragesInStock = finalStock;
        totalBeveragesConsumed = consumption;
        totalBeveragesAdded = added;

        document.getElementById('initialBeveragesStock').textContent = initialStock;
        document.getElementById('finalBeveragesStock').textContent = finalStock;
        document.getElementById('totalBeveragesConsumption').textContent = consumption;
        document.getElementById('totalBeveragesAdded').textContent = added;

        return;
    }

    let initialStock = 0;
    let finalStock = 0;
    let consumption = 0;
    let added = 0;
    items[itemToEvaluate].forEach(item => {
        initialStock += parseInt(item.querySelector('.initialStock').textContent);
        finalStock += parseInt(item.querySelector('.finalStock').textContent);
        consumption += parseInt(item.querySelector('.consumption').textContent);
        added += parseInt(item.querySelector('.added').textContent);
    });

    if (food) {

        if (adding) {
            totalInitialFoodInStock += initialStock;
            totalFinalFoodInStock += finalStock;
            totalFoodConsumed += consumption;
            totalFoodAdded += added;
        } else {
            totalInitialFoodInStock -= initialStock;
            totalFinalFoodInStock -= finalStock;
            totalFoodConsumed -= consumption;
            totalFoodAdded -= added;
        }

        document.getElementById('initialFoodStock').textContent = totalInitialFoodInStock;
        document.getElementById('finalFoodStock').textContent = totalFinalFoodInStock;
        document.getElementById('totalFoodConsumption').textContent = totalFoodConsumed;
        document.getElementById('totalFoodAdded').textContent = totalFoodAdded;
    
    } else if (beverages) {

        if (adding) {
            totalInitialBeveragesInStock += initialStock;
            totalFinalBeveragesInStock += finalStock;
            totalBeveragesConsumed += consumption;
            totalBeveragesAdded += added;
        } else {
            totalInitialBeveragesInStock -= initialStock;
            totalFinalBeveragesInStock -= finalStock;
            totalBeveragesConsumed -= consumption;
            totalBeveragesAdded -= added;
        }

        document.getElementById('inititalBeveragesStock').textContent = totalInitialBeveragesInStock;
        document.getElementById('finalBeveragesStock').textContent = totalFinalBeveragesInStock;
        document.getElementById('totalBeveragesConsumption').textContent = totalBeveragesConsumed;
        document.getElementById('totalBeveragesAdded').textContent = totalBeveragesAdded;
    }
}

function getAverageOfItemsConsumption(food = false, beverages = false, days) {
    let averageStock = 0;
    let averageConsumed = 0;
    let index = 0;

    if (food) {
        nameOfFoodItems.forEach(name => {
            if (foodItemsToShowArray[index]) {
                items[name].forEach(item => {
                    averageStock += parseInt(item.querySelector('.initialStock').textContent);
                    averageConsumed += parseInt(item.querySelector('.totalConsumed').textContent);
                });
            }
            index++;
        });
    } else if (beverages) {
        nameOfBeveragesItems.forEach(name => {
            if (beverageItemsToShowArray[index]) {
                items[name].forEach(item => {
                    averageStock += parseInt(item.querySelector('.initialStock').textContent);
                    averageConsumed += parseInt(item.querySelector('.totalConsumed').textContent);
                });
            }
            index++;
        });
    }

    if (food) {

        document.getElementById('averageFoodInStock').textContent = averageStock;
        document.getElementById('averageFoodExpenses').textContent = averageConsumed;


    } else if (beverages) {

        document.getElementById('averageBeveragesInStock').textContent = averageStock;
        document.getElementById('averageBeveragesExpenses').textContent = averageConsumed;

    }
}