
// data if after 2004 is something like this 
// {'meta_data': [{'id': 1, 'name': 'Bonnie', 'formed_date': 'August 3, 2004', 'dissipated_date': 'August 14, 2004', 'classification': 'Tropical_Storm', 'url': 'https://en.wikipedia.org/wiki/Tropical_Storm_Bonnie_(2004)', 'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/TS_Bonnie_11_aug_2004_1650Z.jpg/220px-TS_Bonnie_11_aug_2004_1650Z.jpg', 'fatalities': '3 direct, 1 indirect', 'damage': '$1.27\xa0million (2004USD)'}"}
    // {'storm_entries': [{'id': 1, ... etc}.. {...}]

   // {'id': 9616, 'codename': 'AL182021', 'date': datetime.date(2021, 9, 23), 'latitude_n': 10.4, 'latitude_w': -36.0, 'maxwind_knots': 35, 'minimum_pressure_mb': 35, 'NE_34kt': 1006, 'SE_34kt': 30, 'SW_34kt': 0, 'NW_34kt': 0, 'NE_50kt': 30, 'SE_50kt': 0, 'SW_50kt': 0, 'NW_50kt': 0, 'NE_64kt': 0, 'SE_64kt': 0, 'SW_64kt': 0, 'NW_64kt': 0, 'radius_max_wind': 35, 'radius_34': 345.3333333333333, 'radius_50': 10.0, 'radius_64': 0.0, 'storm_id': 293},
// but data before 2004 has no 'meta_data' so is something like this
//

import React from 'react';
import { Circle, Polyline, Popup } from 'react-leaflet';

export default function HeatMapIndividual({ data }) {
    const entries = Array.isArray(data) ? data : (data.storm_entries || []);
  
    function convertClassification(initials) {
      if (initials === 'TD') return 'Tropical Depression';
      if (initials === 'TS') return 'Tropical Storm';
      if (initials === 'HU') return 'Hurricane';
      if (initials === 'SD') return 'Subtropical Cyclone';
      if (initials === 'SS') return 'Subtropical Storm';
      //EX: Extratropical Cyclone
      if(initials === 'EX') return 'Extratropical Cyclone';
      //LO: Low Pressure Area
      if(initials === 'LO') return 'Low Pressure Area'
      //WV: Tropical Wave
      if(initials === 'WV') return 'Tropical Wave'
      //DB: Disturbance
      if(initials === 'DB') return 'Disturbance'
      return 'Not classified';
    }
  
    const NM_TO_METERS = 1852;
  
    const getWindRadius = (point, speed) => {
      const keys = [`NE_${speed}kt`, `SE_${speed}kt`, `SW_${speed}kt`, `NW_${speed}kt`];
      const values = keys.map(k => point[k] || 0);
      return Math.max(...values);
    };
  
    const stormColor = '#4a4a4a';
  
    // path for storm track
    const latLngs = entries
      .map(point => {
        const lat = point.latitude_n;
        const lon = point.longitude_w;
        return lat !== null && lon !== null ? [lat, lon] : null;
      })
      .filter(Boolean);
  
    return (
      <>
        {latLngs.length > 1 && (
          <Polyline
            positions={latLngs}
            pathOptions={{ color: stormColor, weight: 2, opacity: 0.7 }}
          />
        )}
  
        {entries.map((point, index) => {
          const lat = point.latitude_n;
          const lon = point.longitude_w;
  
          if (lat === null || lon === null) {
            console.warn('Skipping point due to invalid coordinates:', point);
            return null;
          }
  
          return (
            <React.Fragment key={`${point.codename || point.id}-${index}`}>
              {/* Filled center circle */}
              <Circle
                center={[lat, lon]}
                radius={8000} 
                pathOptions={{
                  color: stormColor,
                  fillColor: stormColor,
                  fillOpacity: 0.8,
                }}
              >
                <Popup>
                  <strong>{point.date_YYYYMMDD}</strong><br />
                  <strong>Time 24hr: {point.time_24hr !== null && point.time_24hr !== undefined
                ? point.time_24hr.toString().padStart(4, '0')
                : 'N/A'}</strong>
                <br />
                  <strong>Current classification: {convertClassification(point.current_classification)}</strong><br />
                  Lat: {lat}°N<br />
                  Lon: {lon}°W<br />
                  Maxwind: {point.maxwind_knots || 'N/A'} kt<br />
                  Min pressure: {point.minimum_pressure_mb || 'N/A'} mb
                </Popup>
              </Circle>
  
              {/* Wind radius 34kt */}
              {getWindRadius(point, 34) > 0 && (
                <Circle
                  center={[lat, lon]}
                  radius={getWindRadius(point, 34) * NM_TO_METERS}
                  pathOptions={{
                    color: 'gold',
                    weight: 1,
                    fillOpacity: 0,
                    dashArray: '4',
                  }}
                  interactive={false}
                />
              )}
  
              {/* Wind radius 50kt */}
              {getWindRadius(point, 50) > 0 && (
                <Circle
                  center={[lat, lon]}
                  radius={getWindRadius(point, 50) * NM_TO_METERS}
                  pathOptions={{
                    color: 'orange',
                    weight: 1,
                    fillOpacity: 0,
                    dashArray: '4',
                  }}
                  interactive={false}
                />
              )}
  
              {/* Wind radius 64kt */}
              {getWindRadius(point, 64) > 0 && (
                <Circle
                  center={[lat, lon]}
                  radius={getWindRadius(point, 64) * NM_TO_METERS}
                  pathOptions={{
                    color: 'red',
                    weight: 1,
                    fillOpacity: 0,
                    dashArray: '4',
                  }}
                  interactive={false}
                />
              )}
            </React.Fragment>
          );
        })}
      </>
    );
  }