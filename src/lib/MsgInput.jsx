import React, { useState } from 'react'

export default function MsgInput(props) {

    const [Message, setMessage] = useState('')

    const sendMsg = (e) => {
        e.preventDefault()
        props.sendMsg(Message)
        setMessage('')
    }

    const setMsg = (e) => {
        setMessage(e.target.value)
    }

    return (
        <div>
            <div className="msg-input">
                <form
                    onSubmit={sendMsg}
                >
                    <input
                        className="MsgInput"
                        placeholder="Type your message and hit Enter"
                        onChange={setMsg}
                        value={Message}
                    />
                </form>
            </div>
        </div>
    )
}
