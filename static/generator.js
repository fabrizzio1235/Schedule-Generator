document.addEventListener("DOMContentLoaded", function(){
    let counterOriginal = document.getElementById("counter-pages");
    let counter = Number(counterOriginal.textContent.trim().split("/")[0]);
    console.log(counter);
    let limit = Number(counterOriginal.textContent.trim().split("/")[1]);
    console.log(limit);
    let current = 0; // [(), (), ()] el iterador de paginas 
    const schedules = window.schedules;
    const data = window.data;
    let days = {monday : [],
                tuesday : [],
                wednesday : [],
                thursday : [],
                friday : []
            }//this save the id's in order of its schedules in each array

    function formathour(stringHour) { //just the beggining of the class
        return Number(stringHour.trim().split(":")[0]);
    }

    function sortSubjects (arr, current, data) {
        days = {monday : [],
                tuesday : [],
                wednesday : [],
                thursday : [],
                friday : []
            }
        let LU = [], MA = [], MI = [], JU = [], VIE = [];
         for (let i = 0; i < arr[current].length; i++) {
            let item = data.find(data => data.id === arr[current][i]);
            if(item.monday != null  )LU.push([formathour(item.monday), item.id]);
            if(item.tuesday != null  )MA.push([formathour(item.tuesday), item.id]);
            if(item.wednesday != null  )MI.push([formathour(item.wednesday), item.id]);
            if(item.thursday != null  )JU.push([formathour(item.thursday), item.id]);
            if(item.friday != null  )VIE.push([formathour(item.friday), item.id]);
        }
        LU.sort((a, b) => a[0] - b[0]); //sort by the first pair
        MA.sort((a, b) => a[0] - b[0]);
        MI.sort((a, b) => a[0] - b[0]);
        JU.sort((a, b) => a[0] - b[0]);
        VIE.sort((a, b) => a[0] - b[0]);
        
        for(let it of LU) days.monday.push(it[1]);
        for(let it of MA) days.tuesday.push(it[1]);
        for(let it of MI) days.wednesday.push(it[1]);
        for(let it of JU) days.thursday.push(it[1]);
        for(let it of VIE) days.friday.push(it[1]);
        console.log(days);
    }

    function showSchedule(arr, current, data) {
        for (let day in days) { //clean up the schedule
        const cell = document.getElementById(day);
            if (cell) {
                cell.textContent = "";
            }
        }
        sortSubjects(arr, current, data);
        
        for (let day in days) {
            for (let id of days[day]) { //day = "monday" or "tuesday" so on...
                const dataItem = data.find(d => d.id === id);
                
                let block = document.createElement("div"); 
                block.className = "class-block"; 
                block.innerHTML = `<strong>${dataItem.subject}</strong><br>${dataItem[day]}`; 
                document.getElementById(day).appendChild(block); 
            }
        }
    }

    showSchedule(schedules, current, data);
    console.log(data);

    let buttonL = document.getElementById("left-button").addEventListener('click', function(){
        if(current > 0) {
            current--;
            showSchedule(schedules, current, data);
            counterOriginal.textContent="";
            counterOriginal.textContent= `${current + 1} / ${limit}`;
        }
    })
    
    let buttonR = document.getElementById("right-button").addEventListener('click', function(){
        if(current < limit-1) {
            current++;
            showSchedule(schedules, current, data);
            counterOriginal.textContent="";
            counterOriginal.textContent= `${current + 1} / ${limit}`;
        }
    })
})