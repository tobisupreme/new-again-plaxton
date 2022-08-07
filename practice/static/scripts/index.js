// Get DOM elements
const form = document.querySelector("#form");
const todo = document.querySelector("#todo");
const errorMessage = document.getElementById("error");
const checkboxes = document.querySelectorAll(".checkbox");
const deleteButtons = document.querySelectorAll(".delete");

// create todo when form is submitted
form.addEventListener("submit", createTodo);

// delete todo item when button is clicked
deleteButtons.forEach((button) => button.addEventListener("click", deleteTodo));

// update todo completed status when checkbox is toggled
checkboxes.forEach((checkbox) => checkbox.addEventListener("change", updateTodoStatus));

// function to create todo when form is submitted
function createTodo(e) {
    e.preventDefault();
    errorMessage.className = "hidden";

    // show error if todo is empty
    const todoDescription = todo.value;
    if (todoDescription.length < 1) {
        throw Error("Todo should not be empty!");
    }

    // Define fetch parameters
    const url = `/todo/add`;
    const request = {
        method: "POST",
        body: JSON.stringify({
            description: todoDescription,
        }),
        headers: { "Content-Type": "application/JSON" },
    };

    // Send request to server endpoint using fetch
    fetch(url, request)
        .then((data) => data.json())
        .then((data) => {
            // get ul
            const ul = document.querySelector(".lists-wrap");

            // create <li></li>
            const li = document.createElement("li");

            // create todo description
            const newTodo = document.createTextNode(data.description);

            // create <input type="checkbox" class="checkbox"/>
            const checkbox = document.createElement("input");
            checkbox.setAttribute("type", "checkbox");
            checkbox.className = "checkbox";

            // create <div class="delete">&cross;</div>
            const div = document.createElement("div");
            div.innerHTML = "&cross;";
            div.className = "delete";
            div.addEventListener("click", deleteTodo);

            // put it all in the <li></li>
            li.appendChild(checkbox);
            li.appendChild(newTodo);
            li.appendChild(div);

            // Put it all in the ul
            ul.appendChild(li);
        })
        .catch((err) => {
            // if error, show error message
            console.log(err);
            errorMessage.className = "";
        });
}

// function to update todo completed status when checkbox is toggled
function updateTodoStatus(e) {
    const todo_id = e.target.dataset.id;
    const completed_status = e.target.checked;

    // Define fetch parameters
    const url = `/todo/${todo_id}/update`;
    const request = {
        method: "POST",
        body: JSON.stringify({
            completed: completed_status,
        }),
        headers: { "Content-Type": "application/json" },
    };

    // Send request to server endpoint using fetch
    fetch(url, request)
        .then((response) => console.log(response.status));
}

// function to delete todo item when button is clicked
function deleteTodo(e) {
    const li = e.target.parentElement;
    const todo_id = e.target.parentElement.firstElementChild.dataset.id;

    // Define fetch parameters
    const url = `/todo/${todo_id}/delete`;
    const request = {
        method: "DELETE",
        body: JSON.stringify({
            todo_id: todo_id,
        }),
        headers: { "Content-Type": "application/json" },
    };

    // Send request to server endpoint using fetch
    fetch(url, request)
        .then((response) => {
            if (response.status == 405) {
                li.remove();
                // window.location.reload();
            } else throw Error;
        })
        .catch((err) => {
            // if error, show error message
            console.log(err);
            errorMessage.className = "";
        });
}
