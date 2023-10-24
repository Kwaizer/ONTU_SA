var formfield = document.getElementById('formfield');

function add(){
  var newFieldDeparture = document.createElement('input');
  var newFieldArrival = document.createElement('input');
  newFieldDeparture.setAttribute('type','text');
  newFieldDeparture.setAttribute('name','arrivaldeparture');
  newFieldDeparture.setAttribute('class','text');
  newFieldDeparture.setAttribute('placeholder','Departure');
  newFieldDeparture.setAttribute('required','');
  newFieldDeparture.setAttribute('autocomplete','off');
  formfield.appendChild(newFieldDeparture);
  newFieldArrival.setAttribute('type','text');
  newFieldArrival.setAttribute('name','arrivaldeparture');
  newFieldArrival.setAttribute('class','text');
  newFieldArrival.setAttribute('placeholder','Arrival');
  newFieldArrival.setAttribute('required','')
  newFieldArrival.setAttribute('autocomplete','off');
  formfield.appendChild(newFieldArrival);
}

function remove(){
  var input_tags = formfield.getElementsByTagName('input');
  if(input_tags.length > 2) {
    formfield.removeChild(input_tags[(input_tags.length) - 1]);
    formfield.removeChild(input_tags[(input_tags.length) - 1]);
  }
}