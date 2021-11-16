function loadGrades() {
    var table = "<table><tr><th>student</th><th>grade</th></tr>";
    var name = document.getElementById("name").value;
    var xhttp = new XMLHttpRequest();
    var student_gradeArr;
    var student_grade;
    var url;
    var i;
    if (name == "") {
        url = "http://localhost:5000/grades"
    }
    else {
        name = name.replaceAll('%', "%25");
        name = name.replaceAll(' ', "%20");
        url = "http://localhost:5000/grades/" + name
    }
    xhttp.open("GET", url, true);
    // xhttp.setRequestHeader('Origin', '*')
    xhttp.send();
    xhttp.onload = function(){
        if (this.status == 404) {
            document.getElementById("bruh").innerHTML = name + " does not exist in gradebook.<br>try again (case sensative)";
            return;
        }
        response = this.responseText;
        response = response.replaceAll('{' , '');
        response = response.replaceAll('}' , '');
        response = response.replaceAll('"' , '');
        student_gradeArr = response.split(',');
        for (i = 0; i < student_gradeArr.length; i++) {
            student_grade = student_gradeArr[i].split(':');
            table = table + "<tr> <td> " + student_grade[0] + "</td><td>" + student_grade[1] +"</td></tr>";
        }
        document.getElementById("bruh").innerHTML = table + "</table>";
    };
}

function addGrade() {
      var name = document.getElementById("addname").value;
      var grade = document.getElementById("addgrade").value;
    if (name == ""){
        document.getElementById("addbruh").innerHTML = "Name cannot be empty";
        return;
    }
    if (grade == ""){
        document.getElementById("addbruh").innerHTML = "Grade cannot be empty";
        return;
    }
    if (isNaN(Number(grade))) {
        document.getElementById("addbruh").innerHTML = "Grade could not be interpreted";
        return;
    }
    console.log(topost);
    var topost = "{\"" + name + "\":" + Number(grade) + "}";
    var url = "http://localhost:5000/grades";
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", url);
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.send(topost);
    xhttp.onload= function() {
        if (this.status == 409) {
            document.getElementById("addbruh").innerHTML = "Student name already has grade";
        }
        if (this.status == 200) {
            document.getElementById("addbruh").innerHTML = "Successfully added " + name;
        }
        console.log(this.response);
    };
}

function delGrade() {
    var name = document.getElementById("delname").value;
    var url = "http://localhost:5000/grades";
    var xhttp = new XMLHttpRequest();
    if (name == "")
        return;
    // name = name.replaceAll('%', "%25");
    // name = name.replaceAll(' ', "%20");
    // url = url + name;
    xhttp.open("DELETE", url);
    xhttp.send(name);
    xhttp.onload= function() {
        if (this.status == 409) {
            document.getElementById("delbruh").innerHTML = "Student name already has grade.";
        }
        if (this.status == 404) {
            document.getElementById("delbruh").innerHTML = "Student does not exist.";
        }
        console.log(this.response);
    };
    name = name.replaceAll("%20", " ");
    document.getElementById("delbruh").innerHTML = name + " has been removed from gradebook";
}

function editGrade() {
    var grade = document.getElementById("editgrade").value;
    var name = document.getElementById("editname").value;
    var nameback = name;
    var url = "http://localhost:5000/grades";
    var xhttp = new XMLHttpRequest();
    var gtfo = 0;
    if (name == "") {
        document.getElementById("editbruh").innerHTML = "Name cannot be empty"; 
        return;
    }
    if (grade == "") {
        document.getElementById("editbruh").innerHTML = "Grade cannot be empty";
        return;
    }
    if (isNaN(Number(grade))) {
        document.getElementById("editbruh").innerHTML = "Grade could not be interpreted";
        return;
    }
    
    // name = name.replaceAll('%', "%25");
    // name = name.replaceAll(' ', "%20");
    // url = url + name;
    xhttp.open("DELETE", url);
    xhttp.send(name);
    xhttp.onload= function() {
        if (this.status == 409) {
            document.getElementById("editbruh").innerHTML = "Student name already has grade.";
            return;
        }
        if (this.status == 404) {
            document.getElementById("editbruh").innerHTML = "Student does not exist.";
            console.log("wat");
            gtfo = 1;
            return;
        }
        if (this.status == 200) {
            name = nameback;
            var topost = "{\"" + name + "\":" + Number(grade) + "}";
            url = "http://localhost:5000/grades";
            xhttp.open("POST", url);
            xhttp.setRequestHeader("Content-Type", "application/json");
            xhttp.send(topost);
            xhttp.onload= function() {
                if (this.status == 200) {
                    document.getElementById("editbruh").innerHTML = "Successfully changed " + name + "\'s grade.";
                }
                console.log(this.response);
            };
            }
            console.log(this.response);
    };
}