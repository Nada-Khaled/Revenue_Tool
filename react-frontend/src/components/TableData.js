import React from "react";
import {BasicTable} from './BasicTable'

export const TableData = (props)=> {

    return (
        <BasicTable data={props.data}></BasicTable>
    );
    
}
 
export default TableData;