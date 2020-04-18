
rl = document.getElementById("recipe-list")

function loadData() {
    searchString = document.getElementById("search-field").value
    searchArray = searchString.split(',');
    getParams = ""
    searchArray.forEach(
        function(item, index){
            if (index > 0){
                getParams += "&ingred=" + item.trim()
            }
            else{
                getParams += "?ingred=" + item.trim()
            }
    });
    console.log(getParams)
    getJSON("/api/v1/recipe/"+getParams,
        function (error, data) {
            data = data["data"] // remove wrapper
            console.log(data)
        },
        null
    );
}

