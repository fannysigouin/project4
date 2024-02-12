// script to run model predictions based on user input and produce price prediction
// button and dropdown objects
const sumbit_button = document.getElementById("submit-button"),
    dropdown_neighbourhood = document.getElementById('dropdown-neighbourhood'),
    dropdown_beds = document.getElementById('dropdown-beds'),
    dropdown_baths = document.getElementById('dropdown-baths'),
    dropdown_dens = document.getElementById('dropdown-dens'),
    dropdown_property_type = document.getElementById('dropdown-property-type');
// disable button element
sumbit_button.disabled = true;

dropdown_neighbourhood.addEventListener("change", stateHandle);
dropdown_beds.addEventListener("change", stateHandle);
dropdown_baths.addEventListener("change", stateHandle);
dropdown_dens.addEventListener("change", stateHandle);
dropdown_property_type.addEventListener("change", stateHandle);


function stateHandle() {
    if (dropdown_neighbourhood.value === "" || dropdown_baths.value === "" || dropdown_dens.value === "" || dropdown_property_type.value === "" || dropdown_beds.value === "") {
        sumbit_button.disabled = true; //button remains disabled
    } else {
        sumbit_button.disabled = false; //button is enabled
    }
}


// assign API URL returning the data for neighbourhood dropdowns to a constant
const nhood_data_url = "/api/get_neighbourhoods";

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

// function to predict output based on user input
async function generateOutput() {
    const neighbourhood = dropdown_neighbourhood.value;
    const beds = dropdown_beds.value;
    const baths = dropdown_baths.value;
    const dens = dropdown_baths.value;
    const property_type = dropdown_property_type.value;

    const predict_url = "/predict_Price?beds=" + beds + "&baths=" + baths + "&dens=" + dens + "&property_type=" + property_type + "&neighbourhood=" + neighbourhood;
    
    const outputElement = document.getElementById('output');
    outputElement.innerHTML = '<span class="spinner-border spinner-border-sm text-primary"></span> Predicting Price. Please wait...'
    
    d3.json(predict_url).then(function(data) {
        // console.log(data);
        outputElement.innerText = data
    });
}
