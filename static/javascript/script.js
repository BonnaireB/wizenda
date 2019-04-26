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
  eventRender: function(event, element) {
    element.append( "<span class='closeon' style='top: -2px; right: 0; background-color: #FFF'>X</span>" );
    element.find(".closeon").click(function() {
       $('#calendar').fullCalendar('removeEvents',event._id);
    });
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
  events: {
    url: 'get-events',
    error: function() {
      $('#script-warning').show();
    }
  },
  loading: function(bool) {
    $('#loading').toggle(bool);
  }
  });
  
  $("#calendar").mouseleave(function(){
    var events ;
    var appdir = "/update-value";
    if (events != $('#calendar').fullCalendar('clientEvents')) {
      var docValues = '[';
      events = $('#calendar').fullCalendar('clientEvents');
      events.forEach(element => {
        var debut = "";
        var fin = "";
        var title= element.title
        if (element.start != null) {
          debut = element.start;
        } 
        if (element.end != null) {
          fin = element.end;
        } 
        var current = '{"allDay": '+ element.allDay+',"start": '+debut+', "end": '+fin+', "title": "'+title+'" },';

        docValues= docValues.concat(current);
        
      });
      docValues = docValues.concat("]");
      docValues = docValues.replace(',]',']');
      console.log(docValues);
      $.ajax({
        type: "POST",
        url: appdir,
        data: JSON.stringify(docValues)
      })
    }
  
  });
})

}
