
var rl

function loadData() {
    rl = document.getElementById("recipe-list")
    // make string of get params for request
    getParams = makeGetParamString() 

    getJSON("/api/v1/recipe/" + getParams,
        function (error, data) {
            data = data["data"] // remove wrapper
            console.log(data)
            renderRecipeList(data)
                
        },
        null
    );
}

function makeGetParamString(){
    searchString = document.getElementById("search-field").value
    searchArray = searchString.split(',');
    getParams = ""
    searchArray.forEach(
        function (item, index) {
            if(item.trim() !== ""){
                if (index > 0) {
                    getParams += "&ingred=" + item.trim()
                }
                else {
                    getParams += "?ingred=" + item.trim()
                }
            }

        });
    return getParams
}

function renderRecipeList(data){
    let keys = Object.keys(data).reverse(); // iterate in reverse order, highest score up top
    rl.innerHTML = ""
    keys.forEach(
        function (key) {
            data1 = data[key]
            ingredString = ""
            data1[3].forEach(
                function(ingred){
                    ingredString += `${ingred}<br>`
                }
            )
            
            recString = `
                <a href="${data1[2]}"> 
                    <div class="card text-white bg-dark mb-3" style="max-width: 100%">
                        <div class="card-body recipe-container">
                            <div class="row">
                                <div class="col-4">
                                    <img class="recipe-img" src="data:image/png;base64,${data1[4]}">
                                </div>
                                <div class="col-7">
                                    <div class="row">
                                        <div class="col">
                                            <span><h4 class="recipe-name">${data1[1]}</h4></span>
                                        </div>
                                    </div>
                                    <div class="row">
                                        <div class="col">
                                        <div class="recipe-ingredients">${ingredString}</div>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="col-1">
                                <span class="recipe-score badge badge-primary badge-pill">${(key*100).toFixed(0) + "%"}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </a>
            
            `
            rl.innerHTML += recString
        })
}