


import { MapContainer, TileLayer} from 'react-leaflet';
import 'leaflet/dist/leaflet.css';


import HurricaneMapOverview from './HurricaneMapOverview';
import HurricaneMapIndividual from './HurricaneMapIndividual';
import HurricaneMapPrediction from './HurricaneMapPrediction';


export default function HurricaneMap({ dataToDisplay, dataType }){

    console.log("HeatMap loaded");

    console.log("HurricaneMap - Data:", dataToDisplay);
    console.log("HurricaneMap - Type:", dataType);

    const isOverview = dataType === 'overview';
    const isIndividual = dataType === 'storm_name_year';
    const isPrediction = dataType === 'prediction'

    const isValidData =
    (isOverview && Array.isArray(dataToDisplay)) ||
    (isIndividual && (Array.isArray(dataToDisplay) || Array.isArray(dataToDisplay.storm_entries))) ||
    (isPrediction && Array.isArray(dataToDisplay));

    if (!isValidData) {
      return <p>Loading map...</p>;
    }
  

    return (
        <MapContainer
        center={[40, -98]}
        zoom={5}
        style={{ height: '650px', width: '1100px', position:'relative', top:'50px', left: '50px' }}
      >
        <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            maxZoom={19}
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            />
        
        {dataType === 'overview' && <HurricaneMapOverview data={dataToDisplay} />}
        {dataType === 'storm_name_year' && <HurricaneMapIndividual data={dataToDisplay} />}
        {dataType === 'prediction' && <HurricaneMapPrediction data={dataToDisplay}/>}


      </MapContainer>
    );
  
  };
