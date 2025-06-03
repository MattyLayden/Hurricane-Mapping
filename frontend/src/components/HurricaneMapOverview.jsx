import { Circle, Popup } from 'react-leaflet';

export default function HeatMapOverview({ data }) {

  function typeStormToColour(stormType) {
    switch (stormType) {
      case 'Hurricane':
        return '#d73027';
      case 'Tropical_Storm':
        return '#fc8d59';
      case 'Tropical_Depression':
        return '#fee08b';
      case 'Subtropical_Storm':
        return '#91bfdb';
      case 'Subtropical_Cyclone':
        return '#4575b4';
      default:
        return '#999999';
    }
  }

  return (
    <>
      {data.map((storm) => (
        <Circle
          key={storm.id}
          center={[storm.centre_latitude_n, storm.centre_longitude_w]}
          radius={storm.radius_from_centre * 1000}
          pathOptions={{
            color: typeStormToColour(storm.highest_classification),
            fillColor: typeStormToColour(storm.highest_classification),
            fillOpacity: 0.4,
          }}
          eventHandlers={{
            mouseover: (e) => {
            e.target.openPopup();
            e.target._path.style.cursor = 'pointer'; 
            },
            mouseout: (e) => {
            e.target.closePopup();
            e.target._path.style.cursor = ''; 
            },
        }}
        >
          <Popup>
            <strong>{storm.name}</strong>
            <br />
            Year: {storm.year}
            <br />
            Classification: {storm.highest_classification}
          </Popup>
        </Circle>
      ))}
    </>
  );
}
