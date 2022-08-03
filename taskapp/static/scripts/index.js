const form = document.getElementById("form");
form.addEventListener("submit", sendReq);

function sendReq(e) {
  e.preventDefault();

  const url = "/tasks/create";
  const request = {
    method: "POST",
    body: JSON.stringify({ task_desc: document.getElementById("task").value }),
    headers: { "Content-Type": "application/json" },
  };

  fetch(url, request)
    .then((res) => res.json())
    .then((data) => {
      console.log(data);
      document.getElementById("error").classList.add("hidden");
      const liItem = document.createElement("li");
      liItem.innerText = data.task_desc;
      document.getElementById("tasks").appendChild(liItem);
    }).catch((err) => {
        document.getElementById("error").classList.remove("hidden");
        console.log(err);
    })
}
