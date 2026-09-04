document.addEventListener("DOMContentLoaded", function(){
    let buttons = document.querySelectorAll(".subject-options");
    let selected = document.getElementById("selected-list");
    let hiddenInput = document.getElementById("input");
    let arrSelected = [];

    function updateSelection(){
        hiddenInput.value = arrSelected.join(",");
    }

    buttons.forEach((btn) => {
        btn.addEventListener("click", function(){
            if(this.style.backgroundColor === ""){ // no selected
                this.style.backgroundColor = "green";

                let btnSelected = document.createElement("button"); //create an new  button to append to show it in th web
                btnSelected.type = "button";
                btnSelected.textContent = this.textContent;
                btnSelected.classList.add("subject-options");
                btnSelected.id = "selected-" + this.id;

                btnSelected.addEventListener("click", function(){ 
                    selected.removeChild(btnSelected); 
                    btn.style.backgroundColor = ""; 
                    arrSelected = arrSelected.filter(it => it !== btn.textContent); 
                    updateSelection(); 
                }); 

                selected.appendChild(btnSelected);

                arrSelected.push(this.textContent);
                updateSelection();
            } else if(this.style.backgroundColor === "green") { // already selected
                this.style.backgroundColor = "";
                let btnToRemove = document.getElementById("selected-" + this.id);
                if (btnToRemove) {
                    selected.removeChild(btnToRemove);
                }

                arrSelected = arrSelected.filter(it => it !== this.textContent);
                
                updateSelection();
            }
        });
    });

    //searcher
    let search = document.getElementById("typesubject");
    search.addEventListener('input', function(){
        let typedchar = document.getElementById("typesubject").value;
        buttons.forEach((btn => {
            btnText = btn.textContent;
            if(!btnText.toLowerCase().startsWith(typedchar.toLowerCase())){
                btn.style.display = "none";
            } else {
                btn.style.display = "inline-block";
            }
        }))

    });

    const submitButton = document.getElementById("submit");
    submitButton.addEventListener('click', function(event) {
        // stop the submit function

        if (arrSelected.length === 0) {
            event.preventDefault();
            document.getElementById("advise-button").textContent = "Select at least 1 subject";
        } else {
            document.getElementById("advise-button").textContent = "";
            const form = document.getElementById("myForm"); // asigna un id a tu form
            form.submit(); 
        }
    });
});
