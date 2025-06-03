import React, { useState } from 'react';

import Button from '@mui/material/Button';
import ButtonGroup from '@mui/material/ButtonGroup';



export default function OptionsBar({ onOptionChange }) {

  const handleOptionClick = (e) => {
    const selectedOption = e.target.id;        
    onOptionChange(selectedOption);      
  }

  return (
    <div className='options-bar'
    style={{
      display: 'flex',
      justifyContent: 'center',
      marginBottom: '16px',
    }}>
    <ButtonGroup
      variant="contained"
      aria-label="Basic button group"
      sx={{
        backgroundColor: '#e0e0e0',
        borderRadius: '8px',
      }}
    >
      <Button id="overview" onClick={handleOptionClick}>Overview</Button>
      <Button id="by-storm" onClick={handleOptionClick}>Storm Name</Button>
      <Button id="by-prediction" onClick={handleOptionClick}>Future Predictions</Button>
    </ButtonGroup>
  </div>
  );
}
