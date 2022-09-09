async function getCandidate(x){
    fetch(`/api/candidates?id=${x.value}`, {
        method: "GET",
        headers: {"Content-type": "application/json;charset=UTF-8"}
    })
        .then(response => response.json()) 
        .then(json => {
            if (json.error == undefined){
                document.getElementById("candidateName").innerHTML = "Nome: "+json.name;
                document.getElementById("candidateImg").src = json.photo;
                document.getElementById("candidateDesc").innerHTML = json.description;
                document.getElementById("candidateParty").innerHTML = "Partido: "+json.party;
                document.getElementById("candidato").style.display = "flex";
            }
            else{
                document.getElementById("candidateName").innerHTML = "";
                document.getElementById("candidateImg").src = "";
                document.getElementById("candidateDesc").innerHTML = "";
                document.getElementById("candidateParty").innerHTML = "";
                document.getElementById("candidato").style.display = "none";
            }
    }); 
    
}

function returnValues(){
    document.getElementById('id_citizen').value = 1;
    document.getElementById('id_candidate').value = document.getElementById('vote').value;
    document.getElementById('id_second_turn').value = false;
}