import { Circle, Popup } from 'react-leaflet';

export default function HurricaneMapPrediction({ data }) {

    // array received as id: 3, latitude: 32.76, longitude: -75.7, mei: -0.563908, month: 5, predicted_storm_radius_km: "1078.9 km", predicted_storm_wind: "47.7 knots", year: 2025

    console.log("Received storm data:", data);

    function classifyStormByWindAndLocation(windString, latitude, longitude) {
        const wind = parseFloat(windString);
        const lat = parseFloat(latitude);
        const lon = parseFloat(longitude);
      
        
        const isLikelySubtropical = (lat > 30 && lon > -50);
      
        if (wind >= 64) return isLikelySubtropical ? 'Subtropical_Cyclone' : 'Hurricane';
        if (wind >= 34) return isLikelySubtropical ? 'Subtropical_Storm' : 'Tropical_Storm';
        if (wind > 0) return 'Tropical_Depression';
        return 'Unknown';
      }


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
            {data.map((storm) => {
        const classification = classifyStormByWindAndLocation(
            storm.predicted_storm_wind,
            storm.latitude,
            storm.longitude
        );

        return (
            <Circle
            key={storm.id}
            center={[storm.latitude, storm.longitude]}
            radius={parseFloat(storm.predicted_storm_radius_km) * 1000}
            pathOptions={{
                color: typeStormToColour(classification),
                fillColor: typeStormToColour(classification),
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
                <br />
                Month: {storm.month}
                <br />
                Classification: {classification}
                <br />
                Expected centre: {storm.latitude}, {storm.longitude}
                <br />
                Expected radius: {storm.predicted_storm_radius_km} 
                <br />
                Predicted highest winds (knots): {storm.predicted_storm_wind}
            </Popup>
            </Circle>
        );
        })}

    </>
  );
}
