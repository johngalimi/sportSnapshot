import React from 'react';

import '.\\styling\\SPAppHeader.css';

export class SPAppHeader extends React.Component {

    render() {
        return (

            <div className = 'header_panel'>

                <h1>
                    <strong>sportSnapshot</strong>
                </h1>
                <h3>
                    <i>Sports data crawled, processed, and visualized</i>
                </h3>

            </div>

        )
    }
}