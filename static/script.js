const file_inp=document.getElementById("resume-input");
const subtitle=document.querySelector(".upload-subtitle")
const uploadBox = document.querySelector(".upload-box");

const roleSection = document.getElementById("roleSection");
const roleSelect = document.getElementById("roleSelect");
const analyseBtn = document.getElementById("analyseBtn");
const form = document.querySelector("form");

file_inp.addEventListener("change",function(){  //UPLOAD LOGIC
    if(file_inp.files.length > 0){
        subtitle.textContent= file_inp.files[0].name + " selected";
        uploadBox.classList.add("active");
        
        //Show dropDown Section
        roleSection.classList.add("show");
        roleSelect.disabled = false;
    }
});

//DRAG AND DROP
uploadBox.addEventListener("dragover",function(e){
    e.preventDefault();
    uploadBox.classList.add("dragover");
});
uploadBox.addEventListener("dragleave",function(e){
    e.preventDefault();
    uploadBox.classList.remove("dragover");
});
uploadBox.addEventListener("drop",function(e){
    e.preventDefault();
    uploadBox.classList.remove("dragover");
    if(e.dataTransfer.files.length >0){
        file_inp.files=e.dataTransfer.files;
        subtitle.textContent=file_inp.files[0].name + " selected";
        uploadBox.classList.add("active");
        
        roleSection.classList.add("show");
        roleSelect.disabled = false;
    }
});

//ROLE SELECTION
roleSection.addEventListener("change",function(){
    if(roleSelect.value !==""){
        analyseBtn.disabled=false;
        analyseBtn.classList.add("enabled");
    }
    else{
        analyseBtn.disabled=true;
        analyseBtn.classList.remove("enabled");
    }
});

form.addEventListener("submit", function () {
    analyseBtn.innerHTML = "Analysing...";
});

