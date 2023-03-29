const weatherData =
{
    "id": 1,
    "city": "College Park",
    "state": 'MD',
    "currentTemp": 32,
    "attribute": 'Clear',
    "localDT": 'Monday, 20 March 2023, 2:29pm EST',
    "d1TempHigh": 62,
    "d1TempLow": 32,
    "d1Attribute": 'Rainy',
    "d2TempHigh": 66,
    "d2TempLow": 47,
    "d2Attribute": 'Cloudy',
    "d3TempHigh": 75,
    "d3TempLow": 52,
    "d3Attribute": 'Sunny',
    "d4TempHigh": 55,
    "d4TempLow": 41,
    "d4Attribute": 'Rainy',
    "d5TempHigh": 57,
    "d5TempLow": 45,
    "d5Attribute": 'Rainy'
}

console.log(weatherData.city);
var city = (weatherData.city);
var state = (weatherData.state);
var currentTemp = (weatherData.currentTemp);
var attribute = (weatherData.attribute);
var localDT = (weatherData.localDT);
var d1TempHigh = (weatherData.d1TempHigh);
var d1TempLow = (weatherData.d1TempLow);
var d1Attribute = (weatherData.d1Attribute);
var d2TempHigh = (weatherData.d2TempHigh);
var d2TempLow = (weatherData.d2TempLow);
var d2Attribute = (weatherData.d2Attribute);
var d3TempHigh = (weatherData.d3TempHigh);
var d3TempLow = (weatherData.d3TempLow);
var d3Attribute = (weatherData.d3Attribute);
var d4TempHigh = (weatherData.d4TempHigh);
var d4TempLow = (weatherData.d4TempLow);
var d4Attribute = (weatherData.d4Attribute);
var d5TempHigh = (weatherData.d5TempHigh);
var d5TempLow = (weatherData.d5TempLow);
var d5Attribute = (weatherData.d5Attribute);

document.getElementById("location").innerHTML = city + ", " + state;
document.getElementById("currentTemp").innerHTML = currentTemp;
document.getElementById("attribute").innerHTML = attribute;
document.getElementById("localDT").innerHTML = localDT;
document.getElementById("d1Temp").innerHTML = d1TempHigh + "° | " + d1TempLow + "°";
document.getElementById("d2Temp").innerHTML = d2TempHigh + "° | " + d2TempLow + "°";
document.getElementById("d3Temp").innerHTML = d3TempHigh + "° | " + d3TempLow + "°";
document.getElementById("d4Temp").innerHTML = d4TempHigh + "° | " + d4TempLow + "°";
document.getElementById("d5Temp").innerHTML = d5TempHigh + "° | " + d5TempLow + "°";

if ((weatherData.attribute).toString() == "Clear") {
    var suggestion = "Don’t forget to wear a jacket!";
}

var message = "Reminder: " + suggestion;
console.log(message);