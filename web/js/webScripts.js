

//setting time label for begin
function setTime() {
document.getElementById("time").innerHTML = "time : " + document.getElementById("time_picker").value + " : 00" ;
}
//setTime();



//changing label for picked time function is called when timeline panel is changed
//changing raster showing hour
function changeTime() {
document.getElementById("time").innerHTML = "time : " + document.getElementById("time_picker").value + " : 00" ;
reloadTiff(document.getElementById("time_picker").value);
}


//changing  color scale  function is called when select box is changed
function changeColorScale(){
console.log(document.getElementById("colorScale").value);
reloadTiff(document.getElementById("time_picker").value, document.getElementById("colorScale").value)
}



// changing data to picked date
// function is called in calendar listener (line +- 100)
function changeDate(date){
    x = date.split("-");
    console.log(x);
    year = x[0];
    month = x [1];
    day = x[2];
    //reloadTiff(x)  na toto treba asi dalsiu metodu tiez
}


function changeSubstance(){
        console.log(document.getElementById("substanceType").value);
}


play = false;


function playAnimation(){
    console.log("animate");
    return;

        colorScale = document.getElementById("colorScale").value;
        while (play){
        //while tu ani nemoe byt, deje sa to na jednom vlakne takze ked sa to pusti
        // neda sa program ovladat teda ani vypnut cyklus
            for (var i = 0; i < 24; i++) {
                //tu by bolo velmi vhodne keby sa dali uz len nie reloadoval
                // ale skor tiff.show(hour)
                // ak to dobre chapem tak sa vzdy vytvara novy komponent
                // toto treba dokodit
//              reloadTiff(i,colorScale);
                console.log(i,"cvak");
                sleep(2000);
            }
        }
}






//sleeping function
function sleep(milliseconds) {
var start = new Date().getTime();
for (var i = 0; i < 1e7; i++) {
  if ((new Date().getTime() - start) > milliseconds){
    break;
  }
}
}







//***calendar javascript***
YUI().use('calendar', 'datatype-date', 'cssbutton',  function(Y) {

    // Create a new instance of calendar, placing it in
    // #mycalendar container, setting its width to 340px,
    // the flags for showing previous and next month's
    // dates in available empty cells to true, and setting
    // the date to today's date.
    var calendar = new Y.Calendar({
      contentBox: "#mycalendar",
      width:'340px',
//      showPrevMonth: true,
//      showNextMonth: true,
      showPrevMonth: false,
      showNextMonth: false,
      date: new Date()}).render();

    // Get a reference to Y.DataType.Date
    var dtdate = Y.DataType.Date;

    // Listen to calendar's selectionChange event.
    calendar.on("selectionChange", function (ev) {

      // Get the date from the list of selected
      // dates returned with the event (since only
      // single selection is enabled by default,
      // we expect there to be only one date)
      var newDate = ev.newSelection[0];

      // Format the date and output it to a DOM
      // element.
//      Y.one("#selecteddate").setHTML(dtdate.format(newDate));
      // this is the call Martin.
      changeDate(dtdate.format(newDate));

    });


});




// new calendar script, not completed, not really correct

//inputObject = document.getElementById("calendar")
//var win = new PopupWindow('mydiv');
//win.autoHide();
//win.setSize(90,90);
//
//
//var cal = new CalendarPopup('mydiv');
//cal.select(inputObject, "calendar",'01/02/2000');
//cal.offsetX = 20;
//cal.offsetY = 20;
//cal.setReturnFunction(myFunction);
//
//function myFunction(y,m,d){
//console.log("myfunctioooon",y,m,d);
//}