
var rl


function checkforURLParam(){
    try {
        let url = window.location.href
        params = url.split("?")[1]
        if (params !== undefined){
            // url param to string for search bar
            params = "?" + params
            loadRecipes(params)
        }
        
      } catch (error) {
        console.log(error)
      }
}


function loadData() {    
    // make string of get params for request
    getParams = makeGetParamString() 
    window.location = window.location.href.split("?")[0] + getParams
}

function loadRecipes(getParams){
    rl = document.getElementById("recipe-list")
    rl.innerHTML = '<div class="loader"></div>'
    document.getElementById("main").className += " data-loaded"

    getJSON("/api/v1/recipe/" + getParams,
    function (error, data) {
        console.log(data)
        ignored = data["data"]["ignored"]
        data = data["data"]["ingred"] // remove wrapper
        
        renderRecipeList(data)
        renderIgnored(ignored)
    },
    function (error, data) {
        console.log(error)
        rl.innerHTML = "<p>Es gab einen Fehler, bitte suchen Sie erneut.</p>"
        insertValueIntoSearchbar()    
    }
);
}
function renderIgnored(ignored){
    document.getElementById("search-form").innerHTML += "<br>"
    ignored.forEach(
        function (item, index) {
            document.getElementById("search-form").innerHTML += `<span class="badge badge-danger badge-pill">${item}</span>`
        }
    )

    insertValueIntoSearchbar()
}

function insertValueIntoSearchbar(){
    let url = window.location.href
    params = url.split("?")[1]
    if (params !== undefined){
        // url param to string for search bar
        paramString = params.split("&").join("").split("ingred=").join(", ").replace(", ", "")
        
        document.getElementById("search-field").value = paramString
        params = "?" + params
        
    }
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
            missingString = ""
            data1[3].forEach(
                function(ingred){
                    if (ingred.charAt(ingred.length-2) === ":"){
                        ingred = ingred.substr(0, ingred.length-2)
                    }
                    ingredString += `${ingred}<br>`
                }
            )
            data1[4].forEach(
                function(ingred){
                    missingString += `${ingred}<br>`
                }
            )
            if(data1[4].length === 0){
                missing = ""  
            }    
            else{
                missing = "<br>Fehlt:<br>"  
            }
                  
            recString = `
                    <div class="card text-white bg-primary mb-3" style="max-width: 100%">
                        <div class="card-body recipe-container">
                            <div class="row">
                                <div class="col-lg-5 col-sm-5 col">
                                    <a href="${data1[2]}" target="_blank"> 
                                        <img class="recipe-img" src="/api/v1/recipe/${data1[0]}/image">
                                    </a>
                                </div>
                                <div class="col-lg col-sm col">
                                    <div class="row">
                                        <div class="col">
                                            <a href="${data1[2]}" target="_blank"> 
                                                <span><h4 class="recipe-name">${data1[1]}</h4></span>
                                            </a>
                                        </div>
                                    </div>
                                    <div class="row">
                                        <div class="col">
                                        <div class="recipe-ingredients">${ingredString}</div>
                                        </div>
                                    </div>
                                    <div class="row">
                                        <div class="col">
                                        ${missing}
                                        <div class="recipe-ingredients missing">
                                            ${missingString}
                                        </div>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="col-lg-1 col-sm-2 col-2">
                                <span class="recipe-score badge badge-info badge-pill">${(key*100).toFixed(0) + "%"}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                
            
            `
            rl.innerHTML += recString
        })
}