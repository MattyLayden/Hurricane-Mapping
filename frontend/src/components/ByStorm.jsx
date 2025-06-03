import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Box, Button, CircularProgress, Autocomplete, TextField } from '@mui/material';

import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import CardActionArea from '@mui/material/CardActionArea';
import CardActions from '@mui/material/CardActions';

export default function ByStorm({ setDataToDisplay, setDataType }) {
    const [yearSelection, setYearSelection] = useState('');
    const [stormName, setStormName] = useState('');
    const [submitLoad, setSubmitLoad] = useState(false);
    const [years, setYears] = useState([]);
    const [stormNames, setStormNames] = useState([]);
    const [metaData, setMetaData] = useState('')
    


    useEffect(() => {
        const yearsArray = [];
        for (let i = 1851; i <= 2023; i++) {
            yearsArray.push(i);
        }
        setYears(yearsArray);
    }, []);

    // NEED TO CHANGE THE APIS ENDPOINTS AND PARAMETERS

    // get_stormnames_from_year should return this json (as .data)
    // {'meta_data': [{'id': 1, 'name': 'Bonnie', 'formed_date': 'August 3, 2004', 'dissipated_date': 'August 14, 2004', 'classification': 'Tropical_Storm', 'url': 'https://en.wikipedia.org/wiki/Tropical_Storm_Bonnie_(2004)', 'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/TS_Bonnie_11_aug_2004_1650Z.jpg/220px-TS_Bonnie_11_aug_2004_1650Z.jpg', 'fatalities': '3 direct, 1 indirect', 'damage': '$1.27\xa0million (2004USD)'}"}
    // {'storm_entries': [{'id': 1, ... etc}.. {...}]

    useEffect(() => {
        if (yearSelection) {
            axios
                .get(`/api/get_stormnames_from_year`, { params: { year: yearSelection } })
                .then((response) => {
                    if (response.status === 200) {
                        
                        setStormNames(response.data.data); //i think its response.data.data not response.data not sure though
                    } else {
                        console.log("Unexpected status code:", response.status);
                        setStormNames([]);
                    }
                })
                .catch((error) => {
                    
                    console.error('Error fetching storm names:', error);
                    setStormNames([]);
                });
        }
    }, [yearSelection]);

    const handleSubmit = async () => {
        try {
            setSubmitLoad(true);
            // 2004 onwards
            if(yearSelection >= 2004){
              const response = await axios.get('/api/get_map_storm_by_name_year_modern/', {
                params: {
                    year: yearSelection,
                    storm_name: stormName,
                },

              
            })
              if (response.status === 200) {
                console.log(`obtained data from handlesubmit function fetching api at 
                  /api/get_map_storm_by_name_year_modern/.... : ${response.data.data}`)
                setDataToDisplay(response.data.data); //maybe .data.data
                setDataType('storm_name_year')
                if (response.data.data.meta_data && response.data.data.meta_data.length > 0) {
                  const firstMeta = response.data.data.meta_data[0];
                  console.log('Setting meta data state to:', firstMeta);
                  setMetaData(firstMeta);
                } else {
                  setMetaData('');
                }
                
                // 
            } else if(response.status === 201) {
                console.log(`obtained data from handlesubmit function fetching api at 
                  /api/get_map_storm_by_name_year_modern/.... : ${response.data.data}`)
                setDataToDisplay(response.data.data);
                setDataType('storm_name_year')
                setMetaData('')
            }else{
              console.error('Error with response:', response);
            }

            }else{
                // before 2004
                const response = await axios.get('/api/get_map_storm_by_name_year_older',{
                  params:{
                    year: yearSelection,
                    storm_name: stormName
                  }
                })

                if(response.status === 200){
                  console.log(`obtained data from handlesubmit function fetching api at 
                    /api/get_map_storm_by_name_year_older/.... : ${response.data.data}`)
                  setDataToDisplay(response.data.data); //maybe .data.data
                  setDataType('storm_name_year')
                  setMetaData('')
                }
            }

        } catch (error) {
            console.error('API fetch error in ByStorm component:', error);
        } finally {
            setSubmitLoad(false);
        }
    };


    const sortedYears = [...years].sort((a, b) => b - a);


    return (
        <Box
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
          <p>Please note that storms from 2004 onwards have more data provided</p>
          <Autocomplete
          value={yearSelection}
          onInputChange={(e, newInputValue) => {
            if (newInputValue) {
              const matchingYear = sortedYears.find(
                (year) => year.toString().startsWith(newInputValue)
              );
              if (matchingYear) {
                setYearSelection(matchingYear);
              }
            }
          }}
          onChange={(e, newValue) => setYearSelection(newValue)}
          options={sortedYears}
          renderInput={(params) => <TextField {...params} label="Year" />}
          getOptionLabel={(option) => option?.toString() || ''}
          sx={{ width: '100%' }}
        />
      
          <Autocomplete
            value={stormName}
            onChange={(e, newValue) => setStormName(newValue)}
            options={stormNames}
            renderInput={(params) => <TextField {...params} label="Storm Name" />}
            getOptionLabel={(option) => option || 'No Storms Available'}
            sx={{ width: '100%' }}
          />
      
          <Button
            variant="outlined"
            onClick={handleSubmit}
            disabled={submitLoad || !yearSelection || !stormName}
            sx={{ width: '100%' }}
          >
            {submitLoad ? <CircularProgress size={24} /> : 'Submit'}
          </Button>

          {metaData && (
            <Card sx={{ maxWidth: 320, mt: 2 }}>
              <CardActionArea>
                <CardMedia
                  component="img"
                  height="140"
                  image={metaData.image}
                  alt="Storm image"
                  onClick={() => window.location.href = metaData.url}
                />
                <CardContent>
                  <Typography variant="body1" fontWeight="bold" sx={{ color: 'text.secondary',  }}>
                    {metaData.name}
                  </Typography>
                  <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                    Formed: {metaData.formed_date}
                  </Typography>
                  <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                    Dissipated: {metaData.dissipated_date}
                  </Typography>
                  <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                    Classification: {metaData.classification.replaceAll('_', ' ')}
                  </Typography>
                  <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                    Fatalities: {metaData.fatalities}
                  </Typography>
                  <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                    Damage: {metaData.damage}
                  </Typography>
                  <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                    Affected areas: {metaData.affected_areas}
                  </Typography>
                </CardContent>
              </CardActionArea>
              <CardActions>
                <Button
                  size="small"
                  color="primary"
                  href={metaData.url}
                  target="_blank"
                >
                  Learn More
                </Button>
              </CardActions>
            </Card>
          )}
        </Box>
      );
}


//{'meta_data': [{'id': 311, 'name': 'Bret', 'formed_date': 'June 19, 2023', 
//'dissipated_date': 'June 24, 2023', 'classification': 'Tropical_Storm',
// 'url': 'https://en.wikipedia.org/wiki/Tropical_Storm_Bret_(2023)', 
// 'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Bret_2023-06-22_1200Z.jpg/250px-Bret_2023-06-22_1200Z.jpg', 
//'fatalities': 'None', 'damage': '>$445,000 (2023USD)', 'affected_areas': 'Windward Islands(mainlyBarbados),Aruba,Colombia'}