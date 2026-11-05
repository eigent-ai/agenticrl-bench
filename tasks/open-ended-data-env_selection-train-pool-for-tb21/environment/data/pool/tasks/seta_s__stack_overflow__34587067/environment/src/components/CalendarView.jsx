import React from 'react';
import { Calendar, momentLocalizer } from 'react-big-calendar';
import moment from 'moment';

const localizer = momentLocalizer(moment);

const DEFAULT_COLOR = '#3174ad';

function CalendarView({ events }) {
  const formattedEvents = events.map(e => ({
    ...e,
    start: new Date(e.start),
    end: new Date(e.end),
  }));

  const styleGetter = (event) => {
    return { style: { backgroundColor: DEFAULT_COLOR } };
  };

  return (
    <div className="calendar-container" style={{ height: 600 }}>
      <Calendar
        localizer={localizer}
        events={formattedEvents}
        startAccessor="start"
        endAccessor="end"
        eventPropGetter={styleGetter}
        style={{ height: '100%' }}
      />
    </div>
  );
}

export default CalendarView;
