const file_inp=document.getElementById("resume-input");
const subtitle=document.querySelector(".upload-subtitle")

file_inp.addEventListener("change",function(){
    if(file_inp.files.length > 0){
        subtitle.textContent= file_inp.files[0].name + " selected";
    }
});