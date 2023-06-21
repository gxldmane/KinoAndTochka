const rangeInput = document.querySelectorAll(".range-input input"),
priceInput = document.querySelectorAll(".price-input input"),
range = document.querySelectorAll(".slider .progress");
let priceGap = 1;
priceInput.forEach(input =>{
 input.addEventListener("input", e =>{
 let minPrice = parseInt(priceInput[0].value),
 maxPrice = parseInt(priceInput[1].value);
        
        if((maxPrice - minPrice >= priceGap) && maxPrice <= rangeInput[1].max){
            if(e.target.className === "input-min"){
 rangeInput[0].value = minPrice;
 range[0].style.left =   (((minPrice - rangeInput[0].min )/ (rangeInput[0].max - rangeInput[0].min))*100) + "%";
            }else{
 rangeInput[1].value = maxPrice;
 range[0].style.right = 100 - ((maxPrice  - rangeInput[1].min) / (rangeInput[1].max - rangeInput[1].min)) * 100 + "%";
            }
        }
    });
});
rangeInput.forEach(input =>{
 input.addEventListener("input", e =>{
 let minVal = parseInt(rangeInput[0].value),
 maxVal = parseInt(rangeInput[1].value);
 let percent = ((minVal)/ (rangeInput[0].max - rangeInput[0].min)) * 100;
 console.log(rangeInput[0].min);
 console.log(percent);
        if((maxVal - minVal) < priceGap){
            if(e.target.className === "range-min"){
 rangeInput[0].value = maxVal - priceGap
            }else{
 rangeInput[1].value = minVal + priceGap;
            }
        }else{
 priceInput[0].value = minVal;
 priceInput[1].value = maxVal;
 range[0].style.left =   (((minVal - rangeInput[0].min )/ (rangeInput[0].max - rangeInput[0].min))*100) + "%";
 range[0].style.right = 100 - ((maxVal  - rangeInput[1].min) / (rangeInput[1].max - rangeInput[1].min)) * 100 + "%";
        }
    });
});



const rangeInput2 = document.querySelectorAll(".range-input2 input"),
priceInput2 = document.querySelectorAll(".price-input2 input"),
range2 = document.querySelector(".slider2 .progress2");
let priceGap2 = 1;

priceInput2.forEach(input =>{
    input.addEventListener("input", e =>{
    let minPrice = parseInt(priceInput[0].value),
    maxPrice = parseInt(priceInput[1].value);
           
           if((maxPrice - minPrice >= priceGap2) && maxPrice <= rangeInput2[1].max){
               if(e.target.className === "input-min"){
    rangeInput2[0].value = minPrice;
    range2.style.left =   ((minPrice / rangeInput2[0].max)*100) + "%";
               }else{
    rangeInput2[1].value = maxPrice;
    range2.style.right = 100 - (maxPrice / rangeInput2[1].max) * 100 + "%";
               }
           }
       });
   });
   rangeInput2.forEach(input =>{
       input.addEventListener("input", e =>{
    let minVal = parseInt(rangeInput2[0].value),
    maxVal = parseInt(rangeInput2[1].value);
           if((maxVal - minVal) < priceGap2){
               if(e.target.className === "range-min"){
    rangeInput2[0].value = maxVal - priceGap2
               }else{
    rangeInput2[1].value = minVal + priceGap2;
               }
           }else{
    priceInput2[0].value = minVal;
    priceInput2[1].value = maxVal;
    range2.style.left =   ((minVal / rangeInput2[0].max)*100) + "%";
    range2.style.right = 100 - (maxVal / rangeInput2[1].max) * 100 + "%";
           }
       });
   });

const smoothLinks = document.querySelectorAll("a[href^='#']");
for (let smoothLink of smoothLinks) {
    smoothLink.addEventListener("click", function (e) {
        e.preventDefault();
        const id = smoothLink.getAttribute("href");

        document.querySelector(id).scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
    });
};
