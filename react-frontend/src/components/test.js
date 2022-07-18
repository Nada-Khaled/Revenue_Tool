import axios from 'axios';

import React,{Component} from 'react';

class App extends Component {


constructor(props) {
        super(props);
    }
    state = {  }
    
    labelStyle={
        fontWeight: 700,
        fontSize: 20,
    }
    
    divStyle={
        marginTop: 55,
    }

    // To make an API call
    SendFiles = async (e) =>{

        e.preventDefault()

        console.log(e.target.files[0])

        const data = new FormData();
        // data.append('file', this.uploadInput.files[0]);
        // data.append('filename', this.fileName.value);

        // fetch('http://localhost:5000/uploadExcelFiles', {
        fetch('http://192.168.1.6:5000/uploadExcelFiles', {
            method: 'POST',
            body: data,
            
        }).then((response) => {
            response.json().then((body) => {
                
                console.log(body);
                
            });
        });
    };
  
    render() { 
        return ( 

            <div className='mt-7 container'>
                
                {/* <form action='http://127.0.0.1:5000/api/uploadExcelFiles' method='POST'> */}
                <form onSubmit={this.SendFiles} encType="multipart/form-data">
                    <div style={this.divStyle}>
                        
                        <label style={this.labelStyle} className="form-label">Upload Site Revenue File:</label>
                        <input className="form-control form-control-lg" id="site-revenue" name="site-revenue" type="file"></input>
                        
                    </div>
                    
                    {/* <div style={divStyle}>
                        
                        <label style={this.labelStyle} className="form-label">Upload Cell Mapping Report:</label>
                        <input className="form-control form-control-lg" id="cell-mapping-report" name="cell-mapping-report" type="file"></input>
                        
                    </div> */}

                    <input className='mt-4 btn btn-primary' type='submit'/>


                </form>

            </div>
        );
    }

}

export default App;
