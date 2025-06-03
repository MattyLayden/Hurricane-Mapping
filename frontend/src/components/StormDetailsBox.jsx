import * as React from 'react';
import { Checkbox } from '@mui/material';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

export default function StormDetailsBox({ rows, setDataToDisplay }) {
  const [selectedRows, setSelectedRows] = React.useState([]);

  React.useEffect(() => {
    if (rows.length > 0) {
      setSelectedRows(rows.map((row) => row.codename));
    }
  }, [rows]);

  const handleCheckboxChange = (event, codename) => {
    const updatedSelected = event.target.checked
      ? [...selectedRows, codename]
      : selectedRows.filter((code) => code !== codename);

    setSelectedRows(updatedSelected);
  };

  React.useEffect(() => {
    const filtered = selectedRows.length > 0
      ? rows.filter((row) => selectedRows.includes(row.codename))
      : rows;

    console.log(`Filtered data in useEffect:`, filtered);

    setDataToDisplay((prevData) => {
      const isSame = JSON.stringify(prevData) === JSON.stringify(filtered);
      return isSame ? prevData : filtered;
    });
  }, [selectedRows, rows, setDataToDisplay]);

  return (
    <TableContainer
      component={Paper}
      sx={{
        maxWidth: '80%',
        margin: '200px auto 20px auto', 
        padding: '0 20px',
      }}
    >
      <Table sx={{ minWidth: 650 }} size="small">
        <TableHead>
          <TableRow>
            <TableCell style={{ fontWeight: 'bold', fontSize: '16px' }}>
              <Checkbox
                checked={selectedRows.length === rows.length}
                onChange={(e) => {
                  if (e.target.checked) {
                    setSelectedRows(rows.map((row) => row.codename));
                  } else {
                    setSelectedRows([]);
                  }
                }}
                indeterminate={
                  selectedRows.length > 0 && selectedRows.length < rows.length
                }
                color="primary"
              />
            </TableCell>
            <TableCell style={{ fontWeight: 'bold', fontSize: '16px' }}>Storm</TableCell>
            <TableCell align="right" style={{ fontWeight: 'bold', fontSize: '16px' }}>
              Year
            </TableCell>
            <TableCell align="right" style={{ fontWeight: 'bold', fontSize: '16px' }}>
              Storm Name
            </TableCell>
            <TableCell align="right" style={{ fontWeight: 'bold', fontSize: '16px' }}>
              Storm Type
            </TableCell>
            <TableCell align="right" style={{ fontWeight: 'bold', fontSize: '16px' }}>
              Latitude - N
            </TableCell>
            <TableCell align="right" style={{ fontWeight: 'bold', fontSize: '16px' }}>
              Longitude - W
            </TableCell>
            <TableCell align="right" style={{ fontWeight: 'bold', fontSize: '16px' }}>
              Radius - M
            </TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row) => (
            <TableRow key={row.codename}>
              <TableCell>
                <Checkbox
                  checked={selectedRows.includes(row.codename)}
                  onChange={(e) => handleCheckboxChange(e, row.codename)}
                  color="primary"
                />
              </TableCell>
              <TableCell>{row.codename}</TableCell>
              <TableCell align="right">{row.year}</TableCell>
              <TableCell align="right">{row.name}</TableCell>
              <TableCell align="right">{row.highest_classification}</TableCell>
              <TableCell align="right">{parseFloat(row.centre_latitude_n).toFixed(2)}</TableCell>
            <TableCell align="right">{parseFloat(row.centre_longitude_w).toFixed(2)}</TableCell>
            <TableCell align="right">{parseFloat(row.radius_from_centre).toFixed(2)}</TableCell>

            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
