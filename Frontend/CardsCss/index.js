const FilterUrl = 'http://127.0.0.1:8050/filter'
let submit = document.getElementById("submitBtn");
let familySelect = document.getElementById("selectFamily");
let variableSelect = document.getElementById("selectVariable");
let countTxt = document.getElementById("count");
let meanTxt = document.getElementById("mean");
let modeTxt = document.getElementById("mode");
let medianaTxt = document.getElementById("mediana");
let stdTxt = document.getElementById("std");
let rangoTxt = document.getElementById("rango");
let withinRangeTxt = document.getElementById("withinRange");
let totalTxt = document.getElementById("total");
let percentage = document.getElementById("percentagewithin");

submit.addEventListener("click", function(){   
    console.log("filtering..",familySelect.value, variableSelect.value)
    GET_FILTERED(familySelect.value, variableSelect.value);
});

function populate(data){
    countTxt.textContent = data.count;
    meanTxt.textContent = data.mean.toFixed(2);
    modeTxt.textContent = data.mode.toFixed(2);
    medianaTxt.textContent = data.median.toFixed(2);
    stdTxt.textContent = data.std.toFixed(2);
    withinRangeTxt.textContent = data.withinRange;
    if(data.min == 'NA'){
        rangoTxt.textContent = data.min;
        percentage.textContent = 0;
        totalTxt.textContent = 0;
    }else{
        rangoTxt.textContent = data.min + " - " + data.max;
        percentage.textContent = ((data.withinRange*100)/data.count).toFixed(2)
        totalTxt.textContent = data.count;
    }
    
}

//AJAX REQUEST TO FILTER
function GET_FILTERED(family,variable){
    const xhttp = new XMLHttpRequest();
    xhttp.open('GET',FilterUrl +'?family='+ family +'&variable=' +variable,true);
    xhttp.send();
    xhttp.onreadystatechange = function(){
        if(this.readyState == 4 && this.status == 200){
            const data = JSON.parse(this.responseText);
            console.log(data);
            populate(data);
            
        }else if(this.readyState == 4 && this.status==400){
            console.log(this.status);
        }
    }    
}