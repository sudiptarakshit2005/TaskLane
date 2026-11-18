
const socket = new WebSocket(
    "ws://" + location.host + "/ws"
);

const statuses = ["todo", "doing", "done"];


socket.onopen = function () {

    document.getElementById("status").textContent =
        "Connected";

};


socket.onclose = function () {

    document.getElementById("status").textContent =
        "Disconnected";

};


socket.onmessage = function (event) {

    const tasks = JSON.parse(event.data);

    showBoard(tasks);

};


function send(message) {

    if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify(message));
    }

}


function makeButton(text, onClick, className = "") {

    const button = document.createElement("button");

    button.textContent = text;

    button.className = className;

    button.onclick = onClick;

    return button;

}


function showBoard(tasks) {

    // Clear all columns

    for (const status of statuses) {

        document.getElementById(status).innerHTML = "";

        document.getElementById(status + "-count").textContent =
            tasks.filter(task => task.status === status).length;

    }


    // Display tasks

    for (const task of tasks) {

        const card = document.createElement("div");

        card.className = "card";


        const title = document.createElement("h3");

        title.textContent = task.title;


        const person = document.createElement("p");

        person.textContent = "Assigned to: " + task.person;


        card.append(title, person);


        const actions = document.createElement("div");

        actions.className = "card-actions";


        const place = statuses.indexOf(task.status);


        // Back button

        if (place > 0) {

            const previous = statuses[place - 1];

            actions.append(

                makeButton("Back", function () {

                    send({
                        action: "move",
                        id: task.id,
                        status: previous
                    });

                })

            );

        }


        // Next button

        if (place < 2) {

            const next = statuses[place + 1];

            actions.append(

                makeButton("Next", function () {

                    send({
                        action: "move",
                        id: task.id,
                        status: next
                    });

                })

            );

        }


        // Delete button

        actions.append(

            makeButton("Delete", function () {

                if (confirm("Are you sure you want to delete this task?")) {

                    send({
                        action: "delete",
                        id: task.id
                    });

                }

            }, "delete")

        );


        card.append(actions);


        document.getElementById(task.status).append(card);

    }

}


// Add task form

document.getElementById("task-form").onsubmit = function (event) {

    event.preventDefault();


    const title = document.getElementById("title").value.trim();

    const person = document.getElementById("person").value.trim();


    if (!title || !person) {

        alert("Please enter task title and assigned person.");

        return;

    }


    send({

        action: "add",

        title: title,

        person: person

    });


    document.getElementById("title").value = "";

    document.getElementById("title").focus();

};
