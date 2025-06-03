import { useState, useEffect } from 'react';
import HurricaneMap from '../components/HurricaneMap';
import OptionsBox from '../components/OptionsBox';

import StormDetailsBox from '../components/StormDetailsBox';


export default function HeatMapPage(){
    const [dataToDisplay, setDataToDisplay] = useState([])
    const [dataType, setDataType] = useState('overview')
    const [tableShow, setTableShow] = useState(true)
    const [initialTableRows, setIniitalTableRows] = useState([])


    useEffect(() => {
        if(dataType == 'overview'){
            setTableShow(true)
        }else{
            setTableShow(false)
        }
    }, [dataType])

    console.log("HeatMapPage - Data to Display:", dataToDisplay);
    console.log("HeatMapPage - Data Type:", dataType); 

    return(
        <>
        
            <HurricaneMap
                 dataToDisplay={dataToDisplay} 
                 dataType={dataType}
                 />

            <OptionsBox
                setDataToDisplay={setDataToDisplay} 
                setDataType={setDataType}
                setIniitalTableRows={setIniitalTableRows}
            />
           {tableShow && <StormDetailsBox
                rows={initialTableRows}
                setDataToDisplay={setDataToDisplay}
           />}  
        </>
    )
}