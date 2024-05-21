import React, { useEffect, useState } from 'react'
import jwt from 'jsonwebtoken'
import { useHistory } from 'react-router-dom'

const UserPage = () => {
	const history = useHistory()

	const centerStyle = {
		margin: "auto",
		width: "50%",
		padding: "10px"
	  }

    const [userList, setuserList] = useState([])
	const [fileList, setfileList] = useState('')
	const [userType, setuserType] = useState('')
	const [userName, setuserName] = useState('')

    async function getUsers() {
        const response = await fetch('http://localhost:8080/user-page', {
			headers: {
				'authorization': 'Bearer ' + localStorage.getItem('token'),
			},
		})

        const data = await response.json()

		console.log("Response data ", data)
		if (data.status == 'success') {
			// if (userType == 'admin') { // have to write logic where admin is able to see all users and select from them}
			setuserList(data.data.userdata)
            console.log("STUFF HERE")
		} else {
			alert(data.message)
		}
    }

    useEffect(() => {
		const token = localStorage.getItem('token')
		if (token) {
			const user = jwt.decode(token)
			if (!user) {
				localStorage.removeItem('token')
				history.replace('/login')

			} else {
				setuserType(user["user_type"])
				setuserName(user["username"])
				getUsers()
			}
		}
	}, [])

	const arrayDataItems = userList.map((user) => (
			<li key={user.file_id}><p>{user.file_name} - {user.file_path} - uploaded on: {user.created_at}</p></li>
			// <span>{user.file_path}</span>
	  ))

	// const arrayDataItems = courses.map((course) => <li>{course}</li>);

    return (
		<div style={centerStyle}>
            <h2>User Page for {userName}</h2>
			<div>
				<h3>List of files uploaded by the user</h3>
			</div>
			<ul>{arrayDataItems}</ul>
        </div>
    )
}

export default UserPage
