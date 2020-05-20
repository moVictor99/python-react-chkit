import React from 'react'
import Msg from './Msg'

import avt from '../static/avt.png'

export default function Msgs(props) {
    return (
        <div>
            <div className="msg">
                <div className="user-info-container">
                    <img
                        alt={props.userName}
                        src={avt}
                        className="msg-avatar"
                    />
                </div>
                <div className="msg-body">
                    <Msg text={props.text} />
                </div>
            </div>
        </div>
    )
}
