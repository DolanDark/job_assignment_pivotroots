import { useState } from 'react'
import { Link } from 'react-router-dom'

function Login() {

	const [email, setEmail] = useState('')
	const [password, setPassword] = useState('')

	const centerStyle = {
		margin: "auto",
		width: "50%",
		padding: "10px"
	  }

	async function loginUser(event) {
		event.preventDefault()

		const response = await fetch('http://localhost:8080/login', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({
				email,
				password,
			}),
		})
		
		const data = await response.json()

		if (data.status == 'success') {
			localStorage.setItem('token', data.data.token)
			alert('Login successful')
			window.location.href = '/userpage'
		} else {
			alert(data.message)
		}
	}

	return (
		<div style={centerStyle}>
			<h1>Login</h1>			
			<form onSubmit={loginUser}>
				<input
					value={email}
					onChange={(e) => setEmail(e.target.value)}
					type="email"
					placeholder="Email"
				/>
				<br />
				<input
					value={password}
					onChange={(e) => setPassword(e.target.value)}
					type="password"
					placeholder="Password"
				/>
				<br />
				<input type="submit" value="Login" />
			</form>
			<br/>
			<Link to="/register"> Dont have an account?</Link>
		</div>
	)
}

export default Login
