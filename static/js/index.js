// adding the data to the form to pass it to server

const MONTHS_WITH_30_DAYS = [1, 3, 5, 7, 8, 10, 12]
const FEBRUARY = 2

window.onbeforeunload = function (event) {  
    $('tr').remove();
};
  

if (document.getElementById('btnResume') != null){
    document.getElementById('btnResume').addEventListener('click', function () {
        document.getElementById('resumeLink').click();
    })
    
    document.getElementById('btnFood').addEventListener('click', function () {
        document.getElementById('foodLink').click()
    })
    
    document.getElementById('btnBeverages').addEventListener('click', function () {
        document.getElementById('beveragesLink').click()
    })
    
    document.getElementById('btnPeople').addEventListener('click', function () {
        document.getElementById('peopleLink').click()
    })
    
    document.getElementById('btnReports').addEventListener('click', function () {
        document.getElementById('reportsLink').click()
    })
}

// when generating reports
// when click in the link in the reports route it will be copied to the clipboard
if (document.getElementsByClassName('linkContainer')[0] != null){
    document.getElementsByClassName('linkContainer')[0].addEventListener('click', function () {
        navigator.clipboard.writeText(document.querySelector('.linkContainer h6').textContent);
        alert("Link copied!");
    });
}

