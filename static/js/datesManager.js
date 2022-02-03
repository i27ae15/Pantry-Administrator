function daysOptionsManager(selectorNumber) {
    monthSelector = $('.monthSelect' + selectorNumber)
    daySelectorOpt = $(`.daySelect${selectorNumber}>option`)
    daySelector = $('.daySelect' + selectorNumber)

    //taking all the select options available in the daySelector to be able to know how many days are there
    let currentAmountOfDayOptions = daySelectorOpt.map(function () {
        return $(this).val();
    }).get();

    // we grab the last index of the amount of days in the input so we can compare how many day there and if depending on the month it needs more or less days or neither
    let indexOfLastDay = currentAmountOfDayOptions.length - 1;

    // adding days to those months that have 31 days but the current options in the select are different do no go up to 31
    if (MONTHS_WITH_30_DAYS.includes(parseInt(monthSelector.val())) &&
        currentAmountOfDayOptions[indexOfLastDay] != '31') {

        lastDay = parseInt(currentAmountOfDayOptions[indexOfLastDay]);
        addDaysToSelect(31, lastDay);

    } else if (!MONTHS_WITH_30_DAYS.includes(parseInt(monthSelector.val())) && parseInt(monthSelector.val()) != FEBRUARY) {
        // getting the month that have 30 days but in the options appear 31 options so we remove that last option

        if (currentAmountOfDayOptions[indexOfLastDay] == '31') {

            daySelectorOpt.each(function () {
                if ($(this).val() == '31') {
                    $(this).remove();
                }
            });
        } else {
            // in case febrary is the month selected then we have to add days instead of remove them 
            lastDay = parseInt(currentAmountOfDayOptions[indexOfLastDay])
            addDaysToSelect(30, lastDay);
        }
    } else if (parseInt(monthSelector.val()) == FEBRUARY) {
        // if febrary was inctroduced them we elimanate the days that do not go with febrary 
        const DAYS_TO_ELIMINATE = ['31', '30', '29']
        daySelectorOpt.each(function () {

            if (DAYS_TO_ELIMINATE.includes($(this).val())) {
                $(this).remove();
            }
        });
    }
}

function addDaysToSelect(top, lastDay) {
    daysToGo = top - lastDay

    for (let n = 0; n < daysToGo; n++) {
        lastDay += 1;
        if (lastDay < 10) {
            lastDay = '0' + String(lastDay);
        }
        daySelector.append($('<option>', {
            value: lastDay,
            text: lastDay
        }));
        lastDay = parseInt(lastDay)

    }
}

//depending on the date we are currenlty at then we add the day, month and year to the inputs
// we should here add the option to the inputs between to increase a day that will appear in th second input option
function selectedOptionsDependingOnDate(day, month, year) {
    for (let selectorNumber = 0; selectorNumber < 3; selectorNumber++) {
        daySelectorOpt = $(`.daySelect${selectorNumber}>option`)
        monthSelectorOpt = $(`.monthSelect${selectorNumber}>option`)
        yearSelectorOpt = $(`.monthSelect${selectorNumber}>option`)

        daySelectorOpt.map(function () {

            if ($(this).val() == day) {
                $(this).attr('selected', true)
            };

        })

        monthSelectorOpt.map(function () {

            if ($(this).val() == month) {
                $(this).attr('selected', true)
            };

        })

        yearSelectorOpt.map(function () {

            if ($(this).val() == year) {
                $(this).attr('selected', true)
            };

        })
    }
}


if (document.getElementById('dateInput') != null) {
    document.getElementById('dateInput').addEventListener('mouseout', function (event) {
        daysOptionsManager(0);
    });
}