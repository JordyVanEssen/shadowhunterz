// -- array of radiobuttons to cycle through
var radiobuttons = [ ];
// -- available functions
var functions = [ ];
// -- websocket
var ws;
// -- webmirror code editor
var editor;

$(document).ready(function(){
	var code = $(".codemirror-textarea")[0];
	editor = CodeMirror.fromTextArea(code, {
        lineNumbers : true,
        mode : "python"
	});
});

// -- opening tabs
function openTab(evt, option) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(option).style.display = "block";
    evt.currentTarget.className += " active";
}

// -- websocket 
function sendData(){
    var color = getColor();

    var json = createJsonObject("Color");
    json.R = color[0];
    json.G = color[1];
    json.B = color[2];

    websocketConnection(JSON.stringify(json));
}

// -- get all the available functions on the Pi
function getAvailableFunctions(){
    var json = createJsonObject("getAll")
    websocketConnection(JSON.stringify(json))
}

// -- create a connection and send/receive data
function websocketConnection(pData) {
    var data = pData;
    var ipAdress = "172.19.3.121";
    var port = "8765";
    ws = new WebSocket(`ws://${ipAdress}:${port}`);

    if ("WebSocket" in window) {

        // Connection opened
        ws.addEventListener('open', function (event) {
            console.log("connnection established");
            ws.send(data);
            console.log("following data sent: ", data)
        });

        // Listen for messages
        ws.addEventListener('message', function (event) {
            var json = JSON.parse(event.data);
            json.functions.forEach(e => {
                if(e.includes('f_')){
                    e = e.substring(2, e.length)
                }
                createRadioButton(e);
            });    
        });

        ws.onclose = function(event) { 
            console.log("connnection closed");
            console.log(event.code);
        };
    } else {
        // The browser doesn't support WebSocket
        alert("WebSocket NOT supported by your Browser!");
    }
}

// -- create a default json object
function createJsonObject(pMode){
    var json = 
    {
        "mode":`${pMode}`
    };
                
    return json;
}

// -- sends the desired function to the Pi
function sendMode(){
    var json = createJsonObject('function');
    // default
    json.function = 'draw'
    radiobuttons.forEach(rb => {
        if(document.getElementById(rb[0]).checked){
            json.function = document.getElementById(rb[0]).value;
            websocketConnection(JSON.stringify(json));
            return;
        }
    });
}

// -- gets the configuration of the panel(s)
function getConfig(){
    var led_X = document.getElementById("ledX").value;
    var led_Y = document.getElementById("ledY").value;
    var square_X = document.getElementById("squareX").value;
    var square_Y = document.getElementById("squareY").value;
    var brightness = document.getElementById("brightness").value;
    var ledCount = document.getElementById("ledCount").value;

    
    var json = createJsonObject("Config");
    json.ledX = led_X;
    json.ledY = led_Y;
    json.squareX = square_X;
    json.squareY = square_Y;
    json.brightness = brightness;
    json.ledCount = ledCount;

    return json;
}

// -- sends the configuration to the Pi
function savePanelSettings(){
    websocketConnection(JSON.stringify(getConfig()));
}

// -- create radiobuttons according to the available functions
function createRadioButton(val){
    if (val == null) {
        val = document.getElementById("customFunctionName").value;
    }
    var id = "r" + (radiobuttons.length + 1);
    var valid = false;
    radiobuttons.forEach(e =>{
        if(e[1] == val){
            valid = true;
        }
    });

    if(!valid){
        var rb = document.createElement("input");
        rb.setAttribute('type', "radio");
        rb.setAttribute('value', val);
        rb.setAttribute('name', 'mode');
        rb.setAttribute('id', id);

        radiobuttons.push([id, val]);
        var form = document.getElementById('radiobuttons');
        form.appendChild(rb);
        form.innerHTML += " " + val + "<br>";
    }
}

// -- sends the customfunction to the Pi
function createFunction(){
    var json = createJsonObject("file");
    json.name = document.getElementById("customFunctionName").value;
    json.customFunction = editor.getValue();
    console.log(json);
    createRadioButton()
    websocketConnection(JSON.stringify(json));
}

 // moduled querySelector
function qs(selectEl){
    return document.querySelector(selectEl);
}

// select RGB inputs
let red = qs('#red'), 
green = qs('#green'), 
blue = qs('#blue'); 

// selet num inputs
let redNumVal = qs('#redNum'), 
greenNumVal = qs('#greenNum'), 
blueNumVal = qs('#blueNum');

// select Color Display
let colorDisplay = qs('#color-display');

// select labels
let redLbl = qs('label[for=red]'), 
greenLbl = qs('label[for=green]'), 
blueLbl = qs('label[for=blue]');

// init display Colors
displayColors();
// init Color Vals
colorNumbrVals();
// init ColorSliderVals
initSliderColors();
// init Change Range Val
changeRangeNumVal();
// init Colors controls
colorSliders();

function getColor(){
    var color = [red.value, green.value, blue.value];
    return color;
}

// display colors
function displayColors(){
    colorDisplay.style.backgroundColor = `rgb(${red.value}, ${green.value}, ${blue.value})`;    
}

// initial color val when DOM is loaded 
function colorNumbrVals(){
    redNumVal.value = red.value;
    greenNumVal.value = green.value;
    blueNumVal.value = blue.value;
}

// initial colors when DOM is loaded
function initSliderColors(){
    // label bg colors
    redLbl.style.background = `rgb(${red.value},0,0)`;
    greenLbl.style.background = `rgb(0,${green.value},0)`;
    blueLbl.style.background = `rgb(0,0,${blue.value})`;

    // slider bg colors
    sliderFill(red);
    sliderFill(green);
    sliderFill(blue);
}

// Slider Fill offset
function sliderFill(clr){
    let val = (clr.value - clr.min) / (clr.max - clr.min);
    let percent = val * 100;

    // clr input
    if(clr === red){
        clr.style.background = `linear-gradient(to right, rgb(${clr.value},0,0) ${percent}%, #cccccc 0%)`;    
    } else if (clr === green) {
        clr.style.background = `linear-gradient(to right, rgb(0,${clr.value},0) ${percent}%, #cccccc 0%)`;    
    } else if (clr === blue) {
        clr.style.background = `linear-gradient(to right, rgb(0,0,${clr.value}) ${percent}%, #cccccc 0%)`;    
    }
}

// change range values by number input
function changeRangeNumVal(){

    // Validate number range
    redNumVal.addEventListener('change', ()=>{
        // make sure numbers are entered between 0 to 255
        if(redNumVal.value > 255){
            alert('cannot enter numbers greater than 255');
            redNumVal.value = red.value;
        } else if(redNumVal.value < 0) {
            alert('cannot enter numbers less than 0');  
            redNumVal.value = red.value;            
        } else if (redNumVal.value == '') {
            alert('cannot leave field empty');
            redNumVal.value = red.value;
            initSliderColors();
            displayColors();
        } else {
            red.value = redNumVal.value;
            initSliderColors();
            displayColors();
        }
    });

    // Validate number range
    greenNumVal.addEventListener('change', ()=>{
        // make sure numbers are entered between 0 to 255
        if(greenNumVal.value > 255){
            alert('cannot enter numbers greater than 255');
            greenNumVal.value = green.value;
        } else if(greenNumVal.value < 0) {
            alert('cannot enter numbers less than 0');  
            greenNumVal.value = green.value;            
        } else if(greenNumVal.value == '') {
            alert('cannot leave field empty');
            greenNumVal.value = green.value;
            initSliderColors();
            displayColors();
        } else {
            green.value = greenNumVal.value;            
            initSliderColors();
            displayColors();
        }
    });

    // Validate number range
    blueNumVal.addEventListener('change', ()=>{
        // make sure numbers are entered between 0 to 255
        if (blueNumVal.value > 255) {
            alert('cannot enter numbers greater than 255');
            blueNumVal.value = blue.value;
        } else if (blueNumVal.value < 0) {
            alert('cannot enter numbers less than 0');
            blueNumVal.value = blue.value;
        } else if(blueNumVal.value == '') {
            alert('cannot leave field empty');
            blueNumVal.value = blue.value;
            initSliderColors();
            displayColors();
        } else {
            blue.value = blueNumVal.value;            
            initSliderColors();
            displayColors();
        }
    });
}

// Color Sliders controls
function colorSliders(){
    red.addEventListener('input', () => {
        displayColors();
        initSliderColors();
        changeRangeNumVal();
        colorNumbrVals();
    });

    green.addEventListener('input', () => {
        displayColors();
        initSliderColors();
        changeRangeNumVal();
        colorNumbrVals();
    });

    blue.addEventListener('input', () => {
        displayColors();
        initSliderColors();
        changeRangeNumVal();
        colorNumbrVals();
    });
}
