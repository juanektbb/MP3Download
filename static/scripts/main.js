var songForm = document.getElementById("songForm");

var submitButton = document.getElementById("submit-button");
var loader = document.getElementById("submit-loader");
var submitAfter = document.getElementById("submit-after");

var superform = document.getElementById("superform");
var superinput = document.getElementById("superinput");

//LISTEN FOR FORM TO BE SUBMITTED
songForm.addEventListener("submit", function(e){
    e.preventDefault()
    var form = e.target

    submitButton.style.display = "none";
    loader.style.display = "block";
    submitAfter.style.display = "none";

    var dataMain = new FormData(form)
    var requestAjax = new XMLHttpRequest()
    
    requestAjax.onreadystatechange = function(){
        try{

            //IF DOWNLOAD IS SUCCESSFUL
            var convertToJSON = JSON.parse(requestAjax.responseText);
            if(convertToJSON.response == "success"){

                //Trigger users download
                superinput.value = convertToJSON.file;
                superform.setAttribute("action", "/trigger");
                superform.submit();

                loader.style.display = "none";
                submitAfter.style.display = "block";

                //AJAX REQUEST TO REMOVE FILE
                var dataForm = new FormData(superform)
                var deleteAjax = new XMLHttpRequest()
                deleteAjax.onreadystatechange = function(){
                    console.log(deleteAjax.responseText)
                }
                deleteAjax.open("POST", "/delete")
                deleteAjax.send(dataForm)
                
            }

        }catch(e){}
    }
    
    requestAjax.open("POST", "/download")
    requestAjax.send(dataMain)
});