// code for make sure that the inputs for the date search have the days accord to the month is selected
// just taking the object inputs and performing the action to increase or decrease the day 
if (document.getElementById('specificDate0') != null) {
    document.getElementById('specificDate0').addEventListener('mouseout', function(event){
        daysOptionsManager(0);
    });

    document.getElementById('specificDate1').addEventListener('mouseout', function(event){
        daysOptionsManager(1);
    });

    document.getElementById('specificDate2').addEventListener('mouseout', function(event){
        daysOptionsManager(2);
    });

    //checking if the final date is bigger than the initial date
    function validateDates() {

        let startDate = new Date(`${$('#yearSelect1').val()}-${$('#monthSelect1').val()}-${$('#daySelect1').val()}`)
        let endDate = new Date(`${$('#yearSelect2').val()}-${$('#monthSelect2').val()}-${$('#daySelect2').val()}`)

        if (startDate >= endDate) {
            alert('The initial date must be less than the final date')
            return false
        }

        return true
    };
} 
