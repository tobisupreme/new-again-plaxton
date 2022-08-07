// Get DOM elements
const root = document.querySelector(":root");
const form = document.querySelector("#form");
const todo = document.querySelector("#todo");
const statusMessage = document.getElementById("status-message");
const deleteButtons = document.querySelectorAll(".delete");

const listsForm = document.querySelector("#list-form");
const todolist = document.querySelector("#todolist");

// create todo when form is submitted
form.addEventListener("submit", createTodo);

// create todolist when form is submitted
listsForm.addEventListener("submit", createTodolist);

// Add click events to delete buttons
function addEventsToDeleteButtons() {
    let deleteButtons = document.querySelectorAll(".delete");

    deleteButtons.forEach((button) => {
        let classList = button.classList;
        classList = Array.from(classList);

        if (classList.indexOf("list") == -1) {
            // delete todo item when button is clicked
            button.addEventListener("click", deleteTodo);
        } else {
            // delete todo list when button is clicked
            button.addEventListener("click", deleteTodolist);
        }
    });
}
addEventsToDeleteButtons();

// Add change events to checkboxes
function addEventsToCheckboxes() {
    const boxes = document.querySelectorAll(".checkbox");
    boxes.forEach((box) => {
        const parentClass = box.parentElement.parentElement.className;
        if (parentClass == "collection-wrap") {
            // update todos in list when checkbox is toggled
            box.addEventListener("change", updateTodosStatusViaList);
        } else if (parentClass == "lists-wrap") {
            // update todo completed status when checkbox is toggled
            box.addEventListener("change", updateTodoStatus);
        }
    });
}
addEventsToCheckboxes();

// function to create todo when form is submitted
function createTodo(e) {
    e.preventDefault();
    statusMessage.className = "hidden";

    // show error if todo is empty
    const todoDescription = todo.value;
    if (todoDescription.length < 1) {
        showError("Todo should not be empty!");
    }

    // Define fetch parameters
    const url = `/todo/add`;
    const request = {
        method: "POST",
        body: JSON.stringify({
            description: todoDescription,
            list_id: e.target[1].value,
        }),
        headers: { "Content-Type": "application/JSON" },
    };

    // Send request to server endpoint using fetch
    fetch(url, request)
        .then((data) => data.json())
        .then((data) => {
            const title = document.querySelector(".list-title").innerText.toLowerCase();
            const listName = data.list_name.toLowerCase();
            if (title == listName) {
                const todoDescription = data.description;
                const todoId = data.id;

                // get ul
                const ul = document.querySelector(".lists-wrap");

                // create <li></li>
                const li = document.createElement("li");

                // create todo description
                const newTodo = document.createTextNode(todoDescription);

                // create <input type="checkbox" data-id="todoId" class="checkbox"/>
                const checkbox = document.createElement("input");
                checkbox.setAttribute("type", "checkbox");
                checkbox.setAttribute("data-id", todoId);
                checkbox.className = "checkbox";

                // create <div class="delete">&cross;</div>
                const div = document.createElement("div");
                div.innerHTML = "&cross;";
                div.className = "delete";

                // put it all in the <li></li>
                li.appendChild(checkbox);
                li.appendChild(newTodo);
                li.appendChild(div);

                // Put it all in the ul
                ul.appendChild(li);
            }

            showSuccess("List successfully added!");
        })
        .then(() => {
            addEventsToCheckboxes();
            addEventsToDeleteButtons();
        })
        .catch((err) => {
            // if error, show error message
            console.table(err);
            showError("Oops! An error occured!");
        });
}

// function to create todolist when form is submitted
function createTodolist(e) {
    e.preventDefault();
    statusMessage.className = "hidden";

    // show error if todolist is empty
    const listname = todolist.value;
    if (listname.length < 1) {
        showError("List title should not be empty!");
    }

    // Define fetch parameters
    const url = `/lists/add`;
    const request = {
        method: "POST",
        body: JSON.stringify({
            name: listname,
        }),
        headers: { "Content-Type": "application/JSON" },
    };

    // Send request to server endpoint using fetch
    fetch(url, request)
        .then((data) => data.json())
        .then((data) => {
            // create <li></li>
            const li = document.createElement("li");

            // create todolist name
            const newTodolist = document.createTextNode(data.listname);
            const anchortag = document.createElement("a");
            anchortag.setAttribute("href", `/lists/${data.list_id}`);
            anchortag.appendChild(newTodolist);

            // create <input type="checkbox" class="checkbox"/>
            const checkbox = document.createElement("input");
            checkbox.setAttribute("data-id", data.list_id);
            checkbox.setAttribute("type", "checkbox");
            checkbox.className = "checkbox";

            // create <div class="delete">&cross;</div>
            const div = document.createElement("div");
            div.innerHTML = "&cross;";
            div.className = "delete";
            div.classList.add("list");

            // put it all in the <li></li>
            li.appendChild(checkbox);
            li.appendChild(anchortag);
            li.appendChild(div);

            // Put it all in the ul
            const collectionWrap = document.querySelector(".collection-wrap");
            collectionWrap.appendChild(li);

            updateTodolistDropdown(data.list_id, data.listname, "add");
        })
        .then(() => {
            addEventsToCheckboxes();
            addEventsToDeleteButtons();
        })
        .catch((err) => {
            // if error, show error message
            console.table(err);
            showError("Oops! An error occured!");
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
    fetch(url, request).then((response) => console.log(response.status));
}

// function to update todos completed status when list checkbox is toggled
function updateTodosStatusViaList(e) {
    const list_id = e.target.dataset.id;
    const lists_status = e.target.checked;

    // Define fetch parameters
    const url = `/lists/${list_id}/update`;
    const request = {
        method: "POST",
        body: JSON.stringify({
            status: lists_status,
        }),
        headers: { "Content-Type": "application/json" },
    };

    // Send request to server endpoint using fetch
    fetch(url, request)
        .then((res) => res.json())
        .then((data) => console.log(data))
        // .then((response) => {
        //     if (response.status == 200) {

        //     }
        // })
        .catch((err) => {
            // if error, show error message
            console.table(err);
            showError("Oops! An error occured!");
        });
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
        .then((response) => response.json())
        .then((response) => {
            if (response.success == true) {
                li.remove();
            } else throw Error;
        })
        .catch((err) => {
            // if error, show error message
            console.table(err);
            showError("Oops! An error occured!");
        });
}

// function to delete todo list when button is clicked
function deleteTodolist(e) {
    const li = e.target.parentElement;
    const list_id = li.firstElementChild.dataset.id;

    // Define fetch parameters
    const url = `/lists/${list_id}/delete`;
    const request = {
        method: "DELETE",
        body: JSON.stringify({
            list_id: list_id,
        }),
        headers: { "Content-Type": "application/json" },
    };

    // Send request to server endpoint using fetch
    fetch(url, request)
        .then((response) => response.json())
        .then((response) => {
            if (response.success == true) {
                li.remove();
                updateTodolistDropdown(list_id, "", "remove");
            } else throw Error;
        })
        .catch((err) => {
            // if error, show error message
            console.table(err);
            showError("Oops! An error occured!");
        });
}

// function to show error message
function showError(msg = "Oops! An error occured!") {
    root.style.setProperty("--status-color", "red");
    statusMessage.innerText = msg;
    statusMessage.classList.remove("hidden");
    throw Error(msg);
}

// function to show success message
function showSuccess(msg) {
    root.style.setProperty("--status-color", "green");
    statusMessage.innerText = msg;
    statusMessage.classList.remove("hidden");
}

// show correct default option on list load
function selectDefaultList() {
    const select = document.querySelectorAll("option");
    const url = window.location.href;
    const matchingRegex = /[.+\/lists/]\d+$/;
    currentListId = url.match(matchingRegex)[0].slice(1);

    select.forEach((option) => {
        if (option.value == currentListId) {
            option.setAttribute("selected", "selected");
        }
    });
}
selectDefaultList();

// update todolist dropdown on change
function updateTodolistDropdown(id, name, action) {
    if (action === "add") {
        // <option value="23">Tambo</option>
        const option = document.createElement("option");
        const listName = document.createTextNode(name);
        option.setAttribute("value", id);
        option.appendChild(listName);
        const select = document.querySelector("select");
        select.appendChild(option);
    } else if (action === "remove") {
        const options = document.querySelectorAll("option");
        options.forEach((option) => {
            if (option.value == id) {
                option.remove();
            }
        });
    }
}
updateTodolistDropdown();
