<!DOCTYPE HTML>

<html>
   <head>
      <link href="css/css.css" rel="stylesheet" type="text/css">
   </head>
   
   <body onload="getAvailableFunctions()">
      <div class="tab">
         <button class="tablinks" onclick="openTab(event, 'changeColor')">Change color</button>
         <button class="tablinks" onclick="openTab(event, 'changeFunction')">Change function</button>
         <button class="tablinks" onclick="openTab(event, 'createFunction')">Create your own function!</button>
         <button class="tablinks" onclick="openTab(event, 'panelConfig')">Panel configuration</button>


      </div>

      <div id="changeColor" class="tabcontent">
         <div class="color-slider-wrap">
            <div class="color-wrap">
                  <div id="color-display"></div>
            </div>
            <div class="sliders">
               <div>
                  <label for="red">Red</label>
                  <input type="number" id="redNum">
                  <input value="200" type="range" min="0" max="255" id="red">
               </div>
               <div>
                  <label for="green">Green</label>
                  <input type="number" id="greenNum">
                  <input value="130" type="range" min="0" max="255" id="green">
               </div>
               <div>
                  <label for="blue">Blue</label>
                  <input type="number" id="blueNum">
                  <input  value="180" type="range" min="0" max="255" id="blue">
               </div>
               <button class="button" type="button" onclick="sendData()">Apply</button>
            </div>
         </div>
      </div>
      
      <div id="panelConfig" class="tabcontent">
         <input type="text" id="ledX" placeholder="aantal leds op de x-as"><br>
         <input type="text" id="ledY" placeholder="aantal leds op de y-as"><br>
         <input type="text" id="squareX" placeholder="aantal hokjes op de x-as"><br>
         <input type="text" id="squareY" placeholder="aantal hokjes op de y-as"><br>
         <input type="text" id="ledCount" placeholder="totaal aantal LEDs"><br>
         <input type="text" id="brightness" placeholder="default helderheid (0-255)"><br>
         <button class="button" type="button" onclick="savePanelSettings()">Save</button>   
      </div>

      <div id="changeFunction" class="tabcontent">
         <form id="radiobuttons" onclick="sendMode()"></form>
      </div>

      <div id="createFunction" class="tabcontent">
         <div class="header-createFunction">
            <input type="text" id="customFunctionName" placeholder="Naam van de functie"><br>
            <button class="button" type="button" onclick="createFunction()">Save function</button>
         </div>
         
         
         <div class="text-editor">
            <textarea id="textArea" class="codemirror-textarea"></textarea>
         </div>
         <div id="error-div" class="error-feedback">

         </div>
      </div>
      
      
      
      <!-- javascript -->
		<script type="text/javascript" src="js/jquery.min.js"></script>
      <script type="text/javascript" src="plugin/codemirror/lib/codemirror.js"></script>
      <script type="text/javascript" src="plugin/codemirror/mode/python/python.js"></script>
      <script type="text/javascript" src="js/main.js"></script>
   </body>
</html>