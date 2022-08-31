async function getCandidate(x){
    let candidate = await fetch(`/api/candidates?id=${x.value}`);
    console.log(candidate)
    return candidate
}