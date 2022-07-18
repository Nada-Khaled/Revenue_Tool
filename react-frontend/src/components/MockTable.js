import React, {useMemo} from 'react'
import {useTable} from 'react-table'
import {TableBody, TableHead, TableRow, TableContainer, Table, TableCell} from '@mui/material'
import {COLUMNS} from './columns'
import {data} from './MOCK_DATA'
import './table.css'

export const MockTable = () =>{

    console.log("in Mock table:")
    console.log(data)

    // useMemo => insures that the data isn't re-created on every
    // render, to improve performance
    const useMemo_columns = useMemo(()=>COLUMNS, [])
    const useMemo_data = useMemo(()=>data, [])

    console.log("use memo data")
    console.log(useMemo_data)

    // console.log("useMemo_data")
    // console.log(useMemo_data)
    
    // specify the columns and the rows(the data which will be rendered)
    // this function will return a table instance which we will store in an instance
    const renderedTable = useTable({
        columns:useMemo_columns,
        data:useMemo_data
    })
    // these are built-in functions and built-in arrays that useTable Hook
    // provides to enable easy table creation
    const {
        getTableProps, // this function will be passed to <table> tag
        getTableBodyProps, // this function will be passed to <tbody> tag
        headerGroups, // this array contains the column heading info which will be passed to <thead> tag
        footerGroups,
        rows,
        prepareRow
        } = renderedTable
        
    // render the table instance that I have just created using useTable Hook
    // I will specify my desired HTML structure
    return(


        <Table {...getTableProps()}>
        <TableHead>
          {headerGroups.map((headerGroup) => (
            <TableRow {...headerGroup.getHeaderGroupProps()}>
              {headerGroup.headers.map((column) => (
                <TableCell {...column.getHeaderProps()}>
                    
                  {column.render("Header")}

                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableHead>
        <TableBody {...getTableBodyProps()}>
          {rows.map((row, idx) => {
            prepareRow(row);

            return (
              <TableRow {...row.getRowProps()}>
                {row.cells.map((cell, idx) => (
                  <TableCell {...cell.getCellProps()}>
                    {cell.render("Cell")}
                  </TableCell>
                ))}
              </TableRow>
            );
          })}
        </TableBody>
      </Table>
    )

} 