var deductBtnArr = document.querySelectorAll('.quantityBtn.minus')
var addButtonArr = document.querySelectorAll('.quantityBtn.plus')
console.log(deductBtnArr);
console.log(addButtonArr);

for (let deductBtn of deductBtnArr) {
    deductBtn.onclick = function () {
        console.log('minus clicked');
        let currentInputBox = deductBtn.nextElementSibling;
        currentInputBox.value = currentInputBox.value - 1;
        if (currentInputBox.value <= 0) {
            currentInputBox.value = 1
        }
    }
}

for (let addButton of addButtonArr) {
    addButton.onclick = () => {
        console.log('plus clicked');
        let currentInputBox = addButton.previousElementSibling;
        currentInputBox.value = parseInt(currentInputBox.value) + 1;
    }
}