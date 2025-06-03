import React, { useState } from 'react';
import Checkbox from '@mui/material/Checkbox';
import FormControlLabel from '@mui/material/FormControlLabel';
import { useEffect } from 'react';


export default function StormTypeCheckboxes({ onStormSelectionChange }) {
  const stormOptions = [
    'All',
    'Hurricane',
    'Tropical_Storm',
    'Tropical_Depression',
    'Subtropical_Cyclone',
    'Subtropical_Storm',
  ];
  const [selected, setSelected] = useState([]);

  useEffect(() => {
    if (onStormSelectionChange) {
      onStormSelectionChange([]); 
    }
  }, []);

  const handleCheckboxChange = (event) => {
    const { value, checked } = event.target;
    let updatedSelected = [...selected];

    if (value === 'All') {
      updatedSelected = checked ? [...stormOptions] : [];
    } else {
      if (checked) {
        updatedSelected.push(value);
      } else {
        updatedSelected = updatedSelected.filter((option) => option !== value);
      }

      const nonAllOptions = stormOptions.filter((opt) => opt !== 'All');
      if (nonAllOptions.every((opt) => updatedSelected.includes(opt))) {
        updatedSelected = [...stormOptions];
      } else {
        updatedSelected = updatedSelected.filter((opt) => opt !== 'All');
      }
    }

    setSelected(updatedSelected);
    console.log(`Selected options: ${updatedSelected}`);

    if (onStormSelectionChange) {
      const toSend = updatedSelected.includes('All')
        ? stormOptions.filter((opt) => opt !== 'All')
        : updatedSelected;

      onStormSelectionChange(toSend);
    }
  };

  return (
    <div className="storm-checkboxes" style={{ display: 'flex', flexDirection: 'column' }}>
      {stormOptions.map((option) => (
        <FormControlLabel
          key={option}
          control={
            <Checkbox
              value={option}
              checked={selected.includes(option)}
              onChange={handleCheckboxChange}
              sx={{
                '& .MuiSvgIcon-root': {
                  color: '#4caf50',
                },
                '&.Mui-checked': {
                  color: '#4caf50',
                },
              }}
            />
          }
          label={option.replace(/_/g, ' ')}
          sx={{
            fontSize: '16px',
            marginBottom: '8px',
            color: '#333',
          }}
        />
      ))}
    </div>
  );
}
