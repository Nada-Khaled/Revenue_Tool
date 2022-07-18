import React, { useMemo } from "react";
import {
  TableCell,
  TableBody,
  TableHead,
  TableRow,
  Table,
} from "@mui/material";
import { useTable, useSortBy } from "react-table";
import { COLUMNS } from "./columns";
import "./table.css";

import { data } from "./MOCK_DATA";

export const BasicTable = (props) => {
  console.log("props in BasicTable:");
  console.log(props.data);

  // useMemo => insures that the data isn't re-created on every
  // render, to improve performance
  const useMemo_columns = useMemo(() => COLUMNS, []);
  const useMemo_data = useMemo(() => props.data, []);

  console.log("useMemo in BasicTable:");
  console.log(useMemo_data);

  // specify the columns and the rows(the data which will be rendered)
  // this function will return a table instance which we will store in an instance
  const renderedTable = useTable(
    {
      columns: useMemo_columns,
      data: useMemo_data,
    },
    useSortBy
  );
  // these are built-in functions and built-in arrays that useTable Hook
  // provides to enable easy table creation
  const {
    getTableProps, // this function will be passed to <table> tag
    getTableBodyProps, // this function will be passed to <tbody> tag
    headerGroups, // this array contains the column heading info which will be passed to <thead> tag
    footerGroups,
    getRowProps,
    rows,
    prepareRow,
  } = renderedTable;

  // render the table instance that I have just created using useTable Hook
  // I will specify my desired HTML structure
  return (
    <table {...getTableProps()}>
      <thead>
        {headerGroups.map((headerGroup) => (
          <tr {...headerGroup.getHeaderGroupProps()}>
            {headerGroup.headers.map((column) => (
              <th {...column.getHeaderProps(column.getSortByToggleProps())}>
                {column.render("Header")}
                <span>
                  {column.isSorted ? (column.isSortedDesc ? "▼" : "▲") : ""}
                </span>
              </th>
            ))}
          </tr>
        ))}
      </thead>
      <tbody {...getTableBodyProps()}>
        {rows.map((row) => {
          prepareRow(row);
          return (
            <tr {...row.getRowProps()}>
              {row.cells.map((cell) => {
                return <td {...cell.getCellProps()}>{cell.render("Cell")}</td>;
              })}
            </tr>
          );
        })}
      </tbody>
      <tfoot>
        {footerGroups.map((footerGroup) => {
          <tr {...footerGroup.getFooterGroupProps()}>
            {footerGroup.headers.map((column) => {
              <td {...column.getFooterProps()}>{column.render("Footer")}</td>;
            })}
          </tr>;
        })}
      </tfoot>
    </table>
  );
};
