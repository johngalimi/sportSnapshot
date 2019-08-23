import React from 'react';

import '.\\styling\\SPAppHeader.css';

export class SPAppHeader extends React.Component {

    render() {
        return (

            <div className = 'main_panel'>

                <h1>sportSnapshot</h1>
                <h3>
                    <i>Sports data crawled, processed, and visualized</i>
                </h3>

            </div>

        )
    }
}