
import { useState, useEffect} from 'react';
import StormTypeCheckboxes from './StormTypeCheckbox';
import YearSlider from './YearSlider'
import axios from 'axios'
import Box from '@mui/material/Box'; 
import Typography from '@mui/material/Typography'; 

import LinearProgress from '@mui/material/LinearProgress';



export default function OverView({setDataToDisplay, setDataType, setIniitalTableRows }) {
    const [stormSelection, setStormSelection] = useState(['All'])
    const [yearSelection, setYearSelection] = useState(2023)
    const [submitLoading, setSubmitLoading] = useState(false)
    const [errorMessage, setErrorMessage] = useState('')

    useEffect(() => {
        async function fetchStorms(){
            try{
                setSubmitLoading(true)

                console.log("stormSelection before fetch:", stormSelection);


                const response = await axios.get('/api/get_heatmap_storms_by_year', {
                    params: {
                    year: yearSelection,
                    storm_type: stormSelection,
                    }
                });
    
                if(response.status === 200){
                    console.log("Fetched Data:", response.data.data);
                    console.log("Fetched data 2:", response.data)
                    setDataToDisplay(response.data.data)
                    setIniitalTableRows(response.data.data)
                    setDataType('overview')
                    // response.data should be  {{"id": 1973, "codename": "AL212023", "year": 2023, "centre_latitude_n": 12.33, etc}}
                }else if(response.status === 404){
                    setDataToDisplay([])
                    setErrorMessage(response.error)
                }
                
            }catch(error){
                console.error('Error fetching data:', error);
                setErrorMessage('Failed to fetch storm data. Please try again later.');
                setDataToDisplay([]);

            }finally{
                setSubmitLoading(false)
            }
        }
        fetchStorms()
    }, [stormSelection, yearSelection])


    

    const onStormSelectionChange = (childValue) => {
        setStormSelection(childValue || []);
      };

    const onYearChange = (childValue) => {
        if(childValue){
            setYearSelection(childValue)
        }
    }


    return (
        <Box
          className="options-div"
          sx={{
            display: 'flex',
            flexDirection: 'column',
            gap: 2,
            alignItems: 'flex-start',
            maxWidth: '320px',
            padding: '16px',
            border: '1px solid #ccc',
            borderRadius: '8px',
            backgroundColor: '#fafafa',
          }}
        >
          <StormTypeCheckboxes onStormSelectionChange={onStormSelectionChange} />
          <YearSlider onYearChange={onYearChange} />
      
          {submitLoading && (
            <LinearProgress
              className="loading-bar"
              sx={{ width: '100%', marginTop: '8px' }}
            />
          )}
        </Box>
      );
}
