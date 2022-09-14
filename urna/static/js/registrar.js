var errors = parseInt(window.location.pathname.split('/')[2],10);
if (errors == 1) {
    alert('Algum erro ocorreu')
}
else if (errors ==2){
    alert("Este RM pertence a outra pessoa")
}