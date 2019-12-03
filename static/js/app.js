
var year = "2015";
var country = "United States";


function buildScatter(sample) {
	d3.json(`/${year}`).then ( data =>{
	  drawScatter(data);
	})
};

function roundNumber(num) {
	return (Math.round(num*100000)/100000);
}


function init() {


	var selector1 = d3.select("#selDataset");
	d3.json("/years").then((sampleYears) => {
    sampleYears.forEach((sample) => {
		selector1
        .append("option")
        .text(sample)
        .property("value", sample);
    });
	})

	var selector2 = d3.select('#selDataset2');
	d3.json("/countries").then((sampleCountries) =>{
	Object.keys(sampleCountries[0]).forEach((country) =>{
		selector2
		.append("option")
		.text(country)
		.property("value", country);
	});
	})

	drawBar()
	buildScatter()

}


function optionChangedOne(newYear) {
	year = newYear;
	d3.select('#scatter').html("");
	buildScatter();
	drawBar();
}
function optionChangedTwo(newCountry) {
	country = newCountry;
	drawBar();
  }
  

init();
