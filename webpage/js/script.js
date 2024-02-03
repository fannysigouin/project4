// script to run model predictions based on user input and produce price prediction

// assign API URL returning the data for dropdowns to a constant

const input_data_url = "http://"

// console log the data to make sure it populates
d3.json(input_data_url).then(function(data) {
    console.log(data);
})

// initialization function to populate dropdowns
function init() {
    // select the dropdown elements from home.html
    let nhood_select = d3.select("dropdown-neighbourhood");
    let beds_select = d3.select("dropdown-beds");
    let baths_select = d3.select("dropdown-baths");
    let dens_select = d3.select("dropdown-dens");

    // append to dropdowns
    d3.json(input_data_url).then(function(data) {
        let nhoods = data.neighbourhoods;
        let beds = data.beds;
        let baths = data.baths;
        let dens = data.dens;
        // loop through neigbourhoods and append to dropdown
        nhoods.forEach((nhood) => {
            nhood_select.append("option").text(nhood).property("value", nhood);
        });
        // loop through beds and append to dropdown
        beds.forEach((bed) => {
            beds_select.append("option").text(bed).property("value", bed);
        });
        // loop through baths and append to dropdown
        baths.forEach((bath) => {
            baths_select.append("option").text(bath).property("value", bath);
        });
        // loop through dens and append to dropdown
        dens.forEach((den) => {
            dens_select.append("option").text(den).property("value", den);
        });
    })
}

// function to load in the model
async function loadModel() {
    const model = "insert_model_file_path_here"
    return model;
}

// function to predict output based on user input
async function generateOutput() {
    const dropdown1 = document.getElementById('dropdown1').value;
    const dropdown2 = document.getElementById('dropdown2').value;
    const dropdown3 = document.getElementById('dropdown3').value;

    // prepare input data
    const inputData = [[dropdown1, dropdown2, dropdown3]]

    // load the model
    const model = await loadModel();

    // get predictions
    const prediction = model.predict(inputData);

    // display predictions
    const outputElement = document.getElementById('output');
    outputElement.innerText = "Predicted Price: $" + prediction
}

// call loadModel function
loadModel();