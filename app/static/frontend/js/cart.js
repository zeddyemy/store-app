var deductBtnArr = document.getElementsByClassName('cartMinus')
var addButtonArr = document.getElementsByClassName('cartPlus')

for (let deductBtn of deductBtnArr) {
    deductBtn.onclick = function () {
        let currentInputBox = deductBtn.nextElementSibling;
        currentInputBox.value = currentInputBox.value - 1;
        if (currentInputBox.value <= 0) {
            currentInputBox.value = 1
        }
    }
}

for (let addButton of addButtonArr) {
    addButton.onclick = () => {
        let currentInputBox = addButton.previousElementSibling;
        currentInputBox.value = parseInt(currentInputBox.value) + 1;
    }
}