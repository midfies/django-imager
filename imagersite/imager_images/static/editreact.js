deleteButton = document.getElementById('delete_button');
deleteButton.addEventListener('click', confirm);
deleteForm = document.getElementById('DeleteConfirm');

function confirm(event) {
    deleteForm.style.display = deleteForm.style.display === '' ? 'block' : '';
    deleteButton.innerText = deleteButton.innerText === 'Delete' ? 'Cancel' : 'Delete';
}