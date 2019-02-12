function loadDoc() {\n\
var xhttp = new XMLHttpRequest();\n\
xhttp.onreadystatechange = function() {\n\
  if (this.readyState == 4 && this.status == 200) {\n\
   document.getElementById("demo").innerHTML = this.responseText;\n\
  }\
};\
xhttp.open("GET", "ajax_info.txt", true);\
xhttp.send();}
