import { useState, useEffect, Component } from 'react'
import axios from 'axios'


export class Chkit extends Component {

    constructor(config) {
        super(config)
        this.BaseURI = config.BaseURI
        this.GetMessagesURI = this.BaseURI + '/get_messages/'
        this.GetMessagesByIdURI = this.GetMessagesURI + config.RoomID + '/'
        this.SendMessageURI = this.BaseURI + '/message/'
        this.roomID = config.RoomID
        this.state = {
            MsgError: []
        }
    }


    // Get Messages using room id provided by client
    getMessagesByRoomID() {
        return axios.get(this.GetMessagesByIdURI)
    }

    getMessagesByUserID(user) {
        const [RetData, setRetData] = useState([])
        useEffect(() => {
            axios.get(this.BaseURI + '/get_messages_by_user/' + user + '/')
                .then(res => {
                    setRetData([...RetData, res.data])
                })
        }, [])
        return RetData
    }

    getMessagesByMsgID(msgID) {
        const [RetData, setRetData] = useState([])
        // useEffect(() => {
        axios.get(this.BaseURI + '/get_messages_by_msg/' + msgID + '/')
            .then(res => {
                setRetData([...RetData, res.data])
            })
        // }, [RetData])
        return RetData
    }

    // Validate message
    ValidateMsg(msg) {
        if (!msg) {
            this.state.MsgError = [...this.state.MsgError, 'Please Type In a message first']
            return false
        } else {
            return true
        }
    }

    sendMessage(mArg) {
        if (this.ValidateMsg(mArg.text)) {
            const msgObj = {
                userID: mArg.userID,
                roomID: this.roomID,
                text: mArg.text,
                tmpID:mArg.tmpID
            }
            let uri = this.SendMessageURI
            const options = {
                method: 'post',
                url: uri,
                data: JSON.stringify(msgObj),
                headers: {
                    'Content-Type': 'application/json',
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                xsrfCookieName: 'XSRF-TOKEN',
                xsrfHeaderName: 'X-XSRF-TOKEN',
                transformRequest: [(data, headers) => {
                    return data;
                }]
            }
            axios(options).catch((err) => console.log(err))
        } else {
            console.error('Please type in the message you wanna send')
        }

    }

}

export default Chkit

