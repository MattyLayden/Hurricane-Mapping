import React, { useState, useEffect, useRef } from 'react';
import { Typography, IconButton, Box, Slider, Stack } from '@mui/material';
import { PlayArrow, Pause, Add, Remove } from '@mui/icons-material';

export default function YearSlider({ onYearChange }) {
  const MIN_YEAR = 1851;
  const MAX_YEAR = 2023;

  const [year, setYear] = useState(MAX_YEAR);
  const [isPlaying, setIsPlaying] = useState(false);
  const intervalRef = useRef(null);

  const updateYear = (newYear) => {
    const clamped = Math.max(MIN_YEAR, Math.min(MAX_YEAR, newYear));
    setYear(clamped);
    onYearChange(clamped);
  };

  const handleSliderChange = (event, newValue) => {
    stopPlaying(); 
    updateYear(newValue);
  };

  const handleIncrement = () => {
    stopPlaying();
    updateYear(year + 1);
  };

  const handleDecrement = () => {
    stopPlaying();
    updateYear(year - 1);
  };

  const togglePlaying = () => {
    if (isPlaying) {
      stopPlaying();
    } else {
      setIsPlaying(true);
    }
  };

  const stopPlaying = () => {
    setIsPlaying(false);
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
  };

  useEffect(() => {
    if (isPlaying) {
      intervalRef.current = setInterval(() => {
        setYear((prevYear) => {
          if (prevYear < MAX_YEAR) {
            const next = prevYear + 1;
            onYearChange(next);
            return next;
          } else {
            stopPlaying();
            return prevYear;
          }
        });
      }, 1500); 
    }

    return () => clearInterval(intervalRef.current);
  }, [isPlaying]);

  return (
    <Box
      className="year-slider-box"
      sx={{
        display: 'flex',
        flexDirection: 'column',
        gap: 2,
        alignItems: 'flex-start',
        width: '100%',
        maxWidth: '320px',
        paddingTop: '8px',
      }}
    >
      <Typography variant="body1" sx={{ fontWeight: 500 }}>
        Year: {year}
      </Typography>

      <Slider
        value={year}
        onChange={handleSliderChange}
        min={MIN_YEAR}
        max={MAX_YEAR}
        step={1}
        valueLabelDisplay="auto"
        aria-label="Year Slider"
        sx={{
          color: '#4caf50',
          width: '100%',
        }}
      />

      <Stack direction="row" spacing={1} alignItems="center">
        <IconButton onClick={handleDecrement} disabled={year <= MIN_YEAR}>
          <Remove />
        </IconButton>

        <IconButton onClick={togglePlaying}>
          {isPlaying ? <Pause /> : <PlayArrow />}
        </IconButton>

        <IconButton onClick={handleIncrement} disabled={year >= MAX_YEAR}>
          <Add />
        </IconButton>
      </Stack>
    </Box>
  );
}
