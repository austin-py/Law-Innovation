const downloadFile = ev => {
    const search_term = document.getElementById("search_term").value;
    console.log(search_term)
    var hiddenElement = document.createElement('a');
    hiddenElement.href = 'data:attachment/text,' + encodeURI(search_term);
    hiddenElement.target = '_blank';
    hiddenElement.download = 'search_term.txt';
    hiddenElement.click();
 //    fetch(`getUser/${username}`).then(function (response) {
 //       return response.text();
 //   }).then(function (text) {
 //       console.log('GET response text:');
 //       console.log(text); 
 //   });
    // console.log(username);
    // goNext(0);
    return search_term;
}