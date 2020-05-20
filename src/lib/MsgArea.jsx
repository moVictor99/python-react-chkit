import React, {useEffect, useRef} from 'react'
import ReactDom from 'react-dom'
import Msgs from './Msgs'


export default function MsgArea(props) {
    
    
    const chatRef = useRef(null)


    useEffect(() => {
        const node = ReactDom.findDOMNode(chatRef.current)
        let ShouldScrollToBottom = node.scrollTop + node.clientHeight + 150 >= node.scrollHeight
        if (ShouldScrollToBottom) {
            node.scrollTop = node.scrollHeight
        }
    })
    
    return (
        <div>
            <div ref={chatRef} className="msg-area">
                {props.msgArr.map((el) => {
                    // message.map((el) =>{
                    return (
                        <div key={el.id || el.tmpID}>
                            <Msgs 
                                userName={el.userID} 
                                text={el.text}
                            />
                        </div>
                    )
                })}
            </div>
        </div>
    )
}
