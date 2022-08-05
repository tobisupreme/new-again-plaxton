const form = document.querySelector("#form");
const todo = document.querySelector("#todo");

form.addEventListener("submit", sendRequest);

function sendRequest(e) {
  e.preventDefault();

  const todoDescription = todo.value;
  if (todoDescription.length < 1) {
    throw Error("Todo should not be empty!");
  }
  const url = `/todo/add`;
  const request = {
    method: "POST",
    body: JSON.stringify({
      description: todoDescription,
    }),
    headers: { "Content-Type": "application/JSON" },
  };

  fetch(url, request)
    .then((data) => data.json())
    .then((data) => console.log(data));
}
