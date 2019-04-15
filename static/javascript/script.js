// Copyright 2019 Bonnaire Benjamin
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.


window.onload = function () {
  $(document).ready(function() {
    $('form')
    var initialLocaleCode = 'fr';
$('#calendar').fullCalendar({
  header: {
    left: 'prev,next today',
    center: 'title',
    right: 'month,agendaWeek,agendaDay,list'
  },
  navLinks: true, // can click day/week names to navigate views
  selectable: true,
  selectHelper: true,
  locale:initialLocaleCode,
  select: function(start, end) {
    var title = prompt('Event Title:');
    var eventData;
    if (title) {
      eventData = {
        title: title,
        start: start,
        end: end
      };
      $('#calendar').fullCalendar('renderEvent', eventData, true); // stick? = true
    }
    $('#calendar').fullCalendar('unselect');
  },
  editable: true,
  eventLimit: true, // allow "more" link when too many events
  events: [
    {
      title: 'Workout',
      start: '2019-04-01'
    },
    {
      title: 'Mon Anniversaire',
      start: '2019-04-03',
    },
    {
      title: 'Conference',
      start: '2019-05-11',
      end: '2019-05-13'
    },
    {
      title: 'Meeting',
      start: '2019-06-12T10:30:00',
      end: '2019-06-12T12:30:00'
    },
    {
      title: 'Lunch',
      start: '2019-04-12T12:00:00'
    },
    {
      title: 'Birthday Party',
      start: '2019-05-13T07:00:00'
    },
    {
      title: 'Click for Google',
      url: 'http://google.com/',
      start: '2019-01-28'
    }
  ]
  
  });
//   $("#calendar").fullCalendar()
// var events ;
//     var appdir = "mon-agenda";
//     var servaddrss = "http://127.0.0.1:5000/";
//     if (events != $('#calendar').fullCalendar('clientEvents')) {
//       var docValues = [{}];
//       events = $('#calendar').fullCalendar('clientEvents');
//       events.forEach(element => {
//         var debut = "";
//         var fin = "";
//         if (element.start != null) {
//           debut = element.start.toString();
//         }
//         if (element.end != null) {
//           fin = element.start.toString();
//         }
//         var current = [{'allDay': element.allDay,'start': debut, 'end':fin, 'title': element.title, }];
//         docValues= docValues.concat(current);
//       });
//       // console.log(JSON.stringify(docValues));
//       $.ajax({
//         type: "POST",
//         url:servaddrss+appdir,
//         data: JSON.stringify(docValues),
//         dataType: 'json'

//       }).done(function(data){
//         console.log("ok");
//         console.log(data);
//       });
//     }
  
  });
}

function addObj(){
  var titre = document.forms["obj_form"]["titre"];
  var nb_heures = document.forms["obj_form"]["nbheures"];
  var freq = document.forms["obj_form"]["freq"];
  if (titre.value == "") {
    return false;
  }else {
  return true;
  }
};
