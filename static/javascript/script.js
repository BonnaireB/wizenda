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

var events ;
var docValues = "[";
  events = $('#calendar').fullCalendar('clientEvents');
  events.forEach(element => {
    docValues += "\n { \n title: '"+ element.title + "', \n" + "allDay: "+ element.allDay + "\n },";

  });
  console.log(docValues);
 

});
}