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
      liItem.innerText = data.description;
      document.getElementById("tasks").appendChild(liItem);
    }).catch((err) => {
        document.getElementById("error").classList.remove("hidden");
        console.log(err);
    })
}
/* fetch("https://dog.ceo/api/breeds/image/random")
    .then(res => res.json()) // parse response as JSON
    .then(data => {
      console.log(data)
    })
    .catch(err => {
        console.log(`error ${err}`)
    });
 */
