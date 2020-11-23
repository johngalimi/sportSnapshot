import React from 'react';

import '.\\styling\\SPAppHeader.css';

export class SPAppHeader extends React.Component {

    render() {
        return (

            <div className = 'header_panel'>

                <h1 className = 'header_panel'>
                    <strong>sportSnapshot</strong>
                </h1>
                <h3 className = 'header_panel'>
                    <i>Sports data crawled, processed, and visualized</i>
                </h3>

            </div>

        )
    }
}