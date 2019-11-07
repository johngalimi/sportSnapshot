import React from 'react';
import { DatePicker } from 'antd';

import '.\\styling\\SPDateSelect.css';

export class SPDateSelect extends React.Component {
    
    render() {
        return (

            <div className = 'date_panel'>

                <h3 className = 'date_panel'>
                    Select a date
                </h3>
                <DatePicker
                    onChange = {this.props.changeHandler}
                    placeholder = {'YYYY-MM-DD'}
                    size = 'large'
                />

            </div>

        )
    }
}