var errors = parseInt(window.location.pathname.split('/')[2],10);

if (errors == 1) {
    alert('RM incorreto');
}
else if (errors == 2) {
    alert('você já votou');
}