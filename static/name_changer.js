const button = document.querySelector('#change_username')
const form = document.querySelector('#update_username')

button.addEventListener("click", () => {

    if(form.style.display === 'none' || form.style.display === "") {
        form.style.display = 'block'
    } else {

        form.style.display = "none";
    }
    
})

form.addEventListener('submit', changeUserName)

function changeUserName(evt){
    evt.preventDefault()
    const formInputs = {
        user_id : document.querySelector('#user_id').value,
        new_username : document.querySelector('#new_username').value
    }
    fetch('/change_username', {
        method: 'POST',
        body: JSON.stringify(formInputs),
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then((response) => response.json()) 
    .then((results) => {
        // alert(results.msg)
        document.querySelector('#username').innerHTML = results.newname
        form.style.display = 'none';
    }
    )
}

