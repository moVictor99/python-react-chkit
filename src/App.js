import React, { useState, useEffect } from 'react';
import './App.css';
import Chkit from './lib/Chkit';
import MsgArea from './lib/MsgArea';
import MsgInput from './lib/MsgInput';

function App() {
    const ChatManeger = new Chkit({
        BaseURI: 'http://localhost:8080',
        RoomID: 1
    })

    const [msgArr, setMsgArr] = useState([])

    useEffect(() => {
        let ret = ChatManeger.getMessagesByRoomID().then((res) => {
            setMsgArr(res.data)
        })
    }, [])


    useEffect(() => {
        const eventSource = new EventSource("http://localhost:8080/get_stream/1/")
        eventSource.addEventListener('newMsg', (e) => {
            if (e.data !== []) {
                updateMsg(e.data)
            }
        })
    }, [msgArr])

    const sendMsg = (msg) => {
        let nMsg = {
            tmpID: Math.random(),
            userID: 'Mohd',
            text: msg
        }
        setMsgArr(msgArr => [...msgArr, nMsg])
        ChatManeger.sendMessage(nMsg)
    }

    const updateMsg = (data) => {
        data = JSON.parse(data)[0]
        setMsgArr(msgArr.filter(msg => msg.tmpID !== data.tmpID))
        setMsgArr(msgArr => [...msgArr, data])
    }

    return (<div>
        <MsgArea msgArr={msgArr} /> <MsgInput sendMsg={sendMsg} />
    </div>
    );
}

export default App;