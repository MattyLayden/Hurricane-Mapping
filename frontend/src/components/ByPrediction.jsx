import React, { useState } from 'react';
import axios from 'axios';
import { Box, Button, CircularProgress, Autocomplete, TextField } from '@mui/material';

export default function ByPrediction({ setDataToDisplay, setDataType }) {
    const [submitLoad, setSubmitLoad] = useState(false);
    const [month, setMonth] = useState('');
    const [emptyMonth, setEmptyMonth] = useState(false);

    const monthSelection = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ];

    async function handleClick() {
        if (!month) {
            setEmptyMonth(true);
            return;
        }

        try {
            setSubmitLoad(true);
            setEmptyMonth(false);

            const response = await axios.get('/api/get_predictions/', {
                params: {
                    month: month
                }
            });

            if (response && response.data && response.data.length > 0) {
                console.log('Obtained data from prediction API:', response.data);
                setDataToDisplay(response.data);
                setDataType('prediction');
            } else {
                console.log('No data returned for selected month.');
                setEmptyMonth(true);
            }
        } catch (error) {
            console.error('Error fetching predictions:', error);
            setEmptyMonth(true);
        } finally {
            setSubmitLoad(false);
        }
    }

    return (
        <>
            <p>Predictions for the year 2025</p>
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
            {emptyMonth && (
                <p style={{ color: 'red' }}>No data predicted for selected month.</p>
            )}

            <Autocomplete
                options={monthSelection}
                value={month}
                onChange={(event, newValue) => setMonth(newValue || '')}
                renderInput={(params) => <TextField {...params} label="Select Month" variant="outlined" />}
                sx={{ width: '100%' }}
                disableClearable
            />

            <Button
                variant="outlined"
                onClick={handleClick} 
                sx={{ width: '100%' }}
                disabled={submitLoad || !month}
            >
                {submitLoad ? <CircularProgress size={24} /> : 'Get Prediction'}
            </Button>
        </Box>
    </>
    );
}