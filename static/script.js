console.log("TaskFlow loaded successfully");

const buttons = document.querySelectorAll(".update-button")

buttons.forEach(function(button){
    button.addEventListener("click", function(event){
        const todoItem = button.closest(".todo-item");
        const input = todoItem.querySelector(".todo-text");

        if (input.hasAttribute("readonly")) {

            event.preventDefault();
    

        input.removeAttribute("readonly");
        input.focus();

        }

    })
})
