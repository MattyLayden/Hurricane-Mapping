
import { useState, useEffect} from 'react';
import OptionsBar from './OptionsBar';
import OverView from './OverView';
import ByPrediction from './ByPrediction';
import ByStorm from './ByStorm';



export default function OptionsBox({ setDataToDisplay, setDataType, setIniitalTableRows }) {
    const [currentOption, setCurrentOption] = useState('overview');

    const onOptionChange = (option) => {
        setCurrentOption(option)
    }
    

    return (
        <div style={{
            position: 'absolute',
            top: '20px',
            right: '20px',
          maxWidth: '400px',  
          margin: '20px auto',
          backgroundColor: '#f0f0f0',
          borderRadius: '10px',
          padding: '16px',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
        }}>
          <OptionsBar onOptionChange={onOptionChange} />
          
         
          {currentOption === 'overview' && <OverView setDataToDisplay={setDataToDisplay} setDataType={setDataType} setIniitalTableRows={setIniitalTableRows} />}
          {currentOption === 'by-storm' && <ByStorm setDataToDisplay={setDataToDisplay} setDataType={setDataType} />}
          {currentOption === 'by-prediction' && <ByPrediction setDataToDisplay={setDataToDisplay} setDataType={setDataType} />}
        </div>
      );
}
