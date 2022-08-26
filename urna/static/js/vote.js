async function getCandidate(x){
    let candidate = await fetch(`/api/candidate?id=${x}`);
    return candidate
}