// script to run model predictions based on user input and produce price prediction

// assign API URL returning the data for neighbourhood dropdowns to a constant

const nhood_data_url = "http://127.0.0.1:5000/api/get_neighbourhoods";

// console log the data to make sure it populates
// d3.json(nhood_data_url).then(function(data) {
//     console.log(data);
// })

// promise function to populate the neighbourhood dropdown
d3.json(nhood_data_url).then(function(data) {
    // select the dropdown element from home.html
    let nhood_select = d3.select("#dropdown-neighbourhood");
    // assign neighourhoods returned from URL to a variable
    let nhoods = data
    // loop through neigbourhoods and append to dropdown
    nhoods.forEach((nhood) => {
        nhood_select.append("option").text(nhood).property("value", nhood);
    });
})

// function to load in the model
async function loadModel() {
    const model = "insert_model_flask_route_here"
    return model;
}

// function to predict output based on user input
async function generateOutput() {
    const neighbourhood = document.getElementById('dropdown-neighbourhood').value;
    const beds = document.getElementById('dropdown-beds').value;
    const baths = document.getElementById('dropdown-baths').value;
    const dens = document.getElementById('dropdown-dens').value;
    const property_type = document.getElementById('dropdown-property-type').value;

    const predict_url = "http://127.0.0.1:5000/predict_Price?beds=" + beds + "&baths=" + baths + "&dens=" + dens + "&property_type=" + property_type + "&neighbourhood=" + neighbourhood;
    
    // fetch(predict_url).then(data => {
    //     const outputElement = document.getElementById('output');
    //     outputElement.innerText = data
    //     console.log(data);
    // });
    
    d3.json(predict_url).then(function(data) {
        console.log(data);
        const outputElement = document.getElementById('output');
        outputElement.innerText = data
    });
}

// call loadModel function
loadModel();