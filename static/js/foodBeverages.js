// Code for make the inputs (are p with contentEditable) in the food and beverages be clean for the backend

let selectedText = null;
let newStockItems = document.querySelectorAll('.newStock');

let permissionLevel = document.getElementById('permissionLevel');

if (permissionLevel != null){
    permissionLevel = permissionLevel.textContent;
    permissionLevel.remove;
}


newStockItems.forEach(element => {
    element.addEventListener('click', event => {
        selectedText = element
    })
});

document.querySelectorAll('.newStock').forEach(item => {
    item.addEventListener('input', clearItemText);
})

function clearItemText(e) {
    // detecting if the text in the selectedText is diferent to numbers
    if (e.data == '' || !/^\d+$/.test(e.data)) {
        selectedText.textContent = selectedText.textContent.replace(/[^\d]/g, '');
        // [optional] make sure focus is on the element
        selectedText.focus();
        // select all the content in the element
        document.execCommand('selectAll', false, null);
        // collapse selection to the end
        document.getSelection().collapseToEnd();

    }
}